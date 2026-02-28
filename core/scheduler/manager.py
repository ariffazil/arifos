"""
core/scheduler/manager.py — Constitutional Agent Scheduler

Integrates the "Eureka" concept of multiplexing LLM access (from AIOS) 
with the strict 13 Constitutional Floors and thermodynamic physics of arifOS.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Awaitable, Callable, Optional

from core.shared.physics import PeaceSquared, W_3_from_tensor, ConstitutionalTensor
from core.shared.types import FloorScores

logger = logging.getLogger(__name__)


@dataclass
class AgentProcess:
    """Represents an active agent requesting cognition time in the scheduler."""

    pid: str  # e.g., "architect_delta_01"
    role: str  # e.g., "ARCHITECT", "ENGINEER", "AUDITOR"
    priority: int = 1  # 0=Critical (Auditor), 1=Standard (Architect/Engineer)
    
    # Execution state
    status: str = "WAITING"  # WAITING, RUNNING, SUSPENDED, COMPLETED
    created_at: datetime = field(default_factory=datetime.now)
    last_run_at: Optional[datetime] = None
    
    # The workload for the current quantum
    coroutine_func: Optional[Callable[..., Awaitable[Any]]] = None
    kwargs: dict[str, Any] = field(default_factory=dict)
    
    # Result tracking
    result: Any = None
    error: Optional[Exception] = None
    
    # Constitutional state
    tensor: Optional[ConstitutionalTensor] = None


class ConstitutionalScheduler:
    """
    A Round-Robin (RR) scheduler that manages Agent 'processes' executing 
    through the governance pipeline, interleaving workloads while 
    enforcing thermodynamic limits (F5 Peace²).
    """

    def __init__(self, quantum_ms: float = 100.0):
        self.quantum_ms = quantum_ms
        
        # Queues based on priority
        self.critical_queue: asyncio.Queue[AgentProcess] = asyncio.Queue()  # Priority 0
        self.standard_queue: asyncio.Queue[AgentProcess] = asyncio.Queue()  # Priority 1
        
        self.active_processes: dict[str, AgentProcess] = {}
        self.is_running = False
        self._loop_task: Optional[asyncio.Task] = None

    async def submit(
        self, 
        pid: str, 
        role: str,
        coro_func: Callable[..., Awaitable[Any]], 
        priority: int = 1,
        **kwargs
    ) -> str:
        """Submit a new agent process for scheduling."""
        if pid in self.active_processes:
            raise ValueError(f"Process {pid} already exists.")
            
        process = AgentProcess(
            pid=pid,
            role=role,
            priority=priority,
            coroutine_func=coro_func,
            kwargs=kwargs
        )
        
        self.active_processes[pid] = process
        
        if priority == 0:
            await self.critical_queue.put(process)
        else:
            await self.standard_queue.put(process)
            
        logger.info(f"Scheduled process {pid} (Role: {role}, Priority: {priority})")
        return pid

    async def start(self):
        """Start the scheduler loop in the background."""
        if self.is_running:
            return
            
        self.is_running = True
        self._loop_task = asyncio.create_task(self._run_loop())
        logger.info("ConstitutionalScheduler started.")

    async def stop(self):
        """Stop the scheduler loop gracefully."""
        self.is_running = False
        if self._loop_task:
            await self._loop_task
        logger.info("ConstitutionalScheduler stopped.")

    async def _run_loop(self):
        """The main Round-Robin interleaved execution loop."""
        while self.is_running:
            # Check critical queue first (Auditor / Validator)
            process = await self._get_next_process()
            
            if not process:
                # No processes ready, sleep briefly
                await asyncio.sleep(0.01)
                continue
                
            await self._execute_quantum(process)

    async def _get_next_process(self) -> Optional[AgentProcess]:
        """Get the next process to run, prioritizing critical over standard."""
        if not self.critical_queue.empty():
            return await self.critical_queue.get()
        if not self.standard_queue.empty():
            return await self.standard_queue.get()
        return None

    async def _execute_quantum(self, process: AgentProcess):
        """Execute a portion of the agent's workload and evaluate physics."""
        process.status = "RUNNING"
        process.last_run_at = datetime.now()
        
        try:
            # We enforce a timeout based on the quantum, however 
            # for IO bound LLM calls, we must allow completion to return control.
            # A true OS scheduler would preempt, but Python async relies on cooperative yield.
            
            logger.debug(f"Executing quantum for {process.pid}")
            
            # Execute the coroutine workload
            if process.coroutine_func:
                result = await asyncio.wait_for(
                    process.coroutine_func(**process.kwargs), 
                    timeout=self.quantum_ms / 1000.0 * 10  # Give 10x multiplier for LLM latency
                )
                
                # Check constitutional state if the process returned a tensor
                if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], ConstitutionalTensor):
                    data, tensor = result
                    process.tensor = tensor
                    process.result = data
                    
                    # Interleaved Physics Evaluation (F5 Peace² sanity check)
                    if not tensor.peace.is_peaceful():
                        logger.warning(f"Process {process.pid} breached Peace² limit! Suspending.")
                        process.status = "SUSPENDED"
                        process.error = ValueError(f"F5 Peace² Breach: {tensor.peace.P2()}")
                        return
                else:
                    process.result = result

                process.status = "COMPLETED"

        except asyncio.TimeoutError:
            # The quantum expired before the agent yielded.
            # We put it back on the queue.
            # In purely CPU bound code this works, for LLM calls they may hold the thread.
            logger.debug(f"Process {process.pid} quantum expired, rescheduling.")
            process.status = "WAITING"
            
            if process.priority == 0:
                await self.critical_queue.put(process)
            else:
                await self.standard_queue.put(process)
                
        except Exception as e:
            logger.error(f"Process {process.pid} faulted: {e}")
            process.status = "SUSPENDED"
            process.error = e

    def get_process_state(self, pid: str) -> Optional[AgentProcess]:
        """Fetch the current state of a scheduled process."""
        return self.active_processes.get(pid)

    async def wait_for_process(self, pid: str) -> Any:
        """Helper to block until a specific process completes."""
        while True:
            process = self.active_processes.get(pid)
            if not process:
                raise ValueError(f"Process {pid} not found.")
                
            if process.status == "COMPLETED":
                return process.result
                
            if process.status == "SUSPENDED":
                raise RuntimeError(f"Process {pid} suspended: {process.error}")
                
            await asyncio.sleep(0.05)
