"""
L5 HYPERVISOR (IGNITION ENGINE)
Drives the continuous metabolic loop of the Agentic Federation.

"Fire requires three things: Fuel (Tokens), Oxygen (Context), and Heat (Ignition)."
"""

import logging
from typing import Any

from .physics import PHYSICS

logger = logging.getLogger("L5_HYPERVISOR")


class Hypervisor:
    """
    The Engine that turns the crank.
    Orchestrates the continuous 000-999 loop.
    """

    def __init__(self) -> None:
        self.running = False
        self.cycle_count = 0

    async def get_fresh_context(self) -> dict[str, Any]:
        """
        Entropy Reset.
        Returns a clean state for the next cycle.
        """
        return {
            "epoch": self.cycle_count,
            "entropy": 0.0,
            "budget_remaining": max(
                0.0, PHYSICS["token"].MAX_SESSION_BUDGET - PHYSICS["token"].session_cost
            ),
        }

    async def cycle(self, agent_instance: Any, input_data: dict[str, Any]) -> dict[str, Any] | Any:
        """
        Execute one metabolic cycle with Physics enforcement.
        """
        self.cycle_count += 1
        logger.info("CYCLE %s: IGNITION", self.cycle_count)

        if not isinstance(input_data, dict):
            return {"verdict": "VOID", "reason": "Input data must be a dictionary"}

        try:
            # 1. Enforce Time Physics (Latency Budget)
            # We wrap the agent's execute method in the TimePhysics measurer
            result = await PHYSICS["time"].measure(agent_instance.execute(input_data))

            # 2. Enforce Token Physics (Energy Budget)
            # STUB: Assume 100 tokens in, 100 tokens out for now
            cost = PHYSICS["token"].consume(100, 100)
            logger.info("CYCLE %s: COMPLETE | Cost: $%.4f", self.cycle_count, cost)

            return result

        except TimeoutError:
            logger.error("CYCLE %s: TIMEOUT (Sabotage Protocol)", self.cycle_count)
            return {"verdict": "SABAR", "reason": "Timeout"}

        except PermissionError as e:
            logger.error("CYCLE %s: STARVATION (%s)", self.cycle_count, e)
            return {"verdict": "VOID", "reason": "Budget Exceeded"}

        except Exception as e:
            logger.exception("CYCLE %s: UNEXPECTED ERROR", self.cycle_count)
            return {"verdict": "VOID", "reason": str(e)}

    async def ignition(self, agent_class: Any, query: str) -> dict[str, Any] | Any:
        """
        The Spark.
        Starts the loop for a specific agent.
        """
        logger.info("IGNITING %s...", getattr(agent_class, "name", "unknown_agent"))
        self.running = True

        # Instantiate Agent
        agent = agent_class()

        # Single Cycle for Demonstration (Infinite loop in production)
        ctx = await self.get_fresh_context()
        ctx["query"] = query

        result = await self.cycle(agent, ctx)

        return result


# Expose singleton
HYPERVISOR = Hypervisor()
