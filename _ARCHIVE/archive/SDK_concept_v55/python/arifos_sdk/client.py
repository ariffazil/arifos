"""
arifOS SDK Client — Interface to Constitutional Gateway.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import asyncio
import os
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import httpx

from .exceptions import (
    ArifOSError,
    FloorViolationError,
    GatewayConnectionError,
    HumanApprovalTimeoutError,
)
from .types import (
    ActorType,
    GatewayDecision,
    HumanApprovalRequest,
    HumanApprovalResponse,
    SessionContext,
    ToolClass,
    Verdict,
)


class ArifOSClient:
    """
    Client for arifOS Constitutional Gateway.

    Usage:
        client = ArifOSClient(
            gateway_url="https://aaamcp.arif-fazil.com",
            api_key="your-api-key",
        )

        session = client.create_session(
            actor_id="arif@arif-fazil.com",
            actor_type="human",
        )

        result = await session.check_action("k8s_apply", payload={...})
    """

    DEFAULT_URL = "https://aaamcp.arif-fazil.com"

    def __init__(
        self,
        gateway_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.gateway_url = gateway_url or os.environ.get("ARIFOS_GATEWAY_URL", self.DEFAULT_URL)
        self.api_key = api_key or os.environ.get("ARIFOS_API_KEY")
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=self.gateway_url,
            headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
            timeout=timeout,
        )

    async def check_action(
        self,
        tool_name: str,
        payload: Dict[str, Any],
        session_id: Optional[str] = None,
        actor_id: Optional[str] = None,
    ) -> GatewayDecision:
        """
        Check if an action passes constitutional floors.

        Args:
            tool_name: Name of the tool to invoke
            payload: Tool-specific parameters
            session_id: Optional session ID (generated if not provided)
            actor_id: Optional actor ID

        Returns:
            GatewayDecision with verdict and floor results

        Raises:
            GatewayConnectionError: If gateway is unreachable
            FloorViolationError: If HARD floors failed (VOID)
        """
        session_id = session_id or f"sdk-{uuid.uuid4().hex[:12]}"

        try:
            response = await self._client.post(
                "/gateway/route_tool",
                json={
                    "tool_name": tool_name,
                    "payload": payload,
                    "session_id": session_id,
                    "actor_id": actor_id or "sdk-user",
                },
            )
            response.raise_for_status()
            data = response.json()

            return self._parse_decision(data, session_id, tool_name)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise FloorViolationError(f"Floor violation: {e.response.text}")
            raise GatewayConnectionError(f"Gateway error: {e}")
        except httpx.ConnectError as e:
            raise GatewayConnectionError(f"Cannot connect to gateway: {e}")

    async def request_human_approval(
        self,
        decision: GatewayDecision,
        notify_channels: Optional[List[str]] = None,
    ) -> HumanApprovalRequest:
        """
        Request human approval for 888_HOLD.

        Args:
            decision: The GatewayDecision that resulted in 888_HOLD
            notify_channels: Channels to notify ("slack", "email", "web")

        Returns:
            HumanApprovalRequest with hold_id and review URL
        """
        if decision.verdict != Verdict.HOLD_888:
            raise ValueError(f"Expected 888_HOLD verdict, got {decision.verdict}")

        hold_id = f"HOLD-{uuid.uuid4().hex[:16].upper()}"

        request = HumanApprovalRequest(
            hold_id=hold_id,
            session_id=decision.session_id,
            tool_name=decision.tool_name,
            payload={},  # Would be populated from original request
            blast_radius=decision.blast_radius,
            floors_failed=decision.hard_failures,
            reasoning=decision.reasoning,
            requested_by=decision.session_id,
            requested_at=datetime.utcnow().isoformat(),
            review_url=f"{self.gateway_url}/approve/{hold_id}",
        )

        # Notify channels
        if notify_channels:
            await self._notify_channels(request, notify_channels)

        return request

    async def await_human_approval(
        self,
        hold_id: str,
        timeout: Optional[float] = None,
        poll_interval: float = 5.0,
    ) -> HumanApprovalResponse:
        """
        Block and wait for human approval.

        Args:
            hold_id: The hold ID from request_human_approval
            timeout: Maximum time to wait (None = infinite)
            poll_interval: Seconds between polls

        Returns:
            HumanApprovalResponse with final verdict

        Raises:
            HumanApprovalTimeoutError: If timeout reached
        """
        start_time = datetime.utcnow()

        while True:
            try:
                response = await self._client.get(f"/gateway/holds/{hold_id}")
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "resolved":
                    return HumanApprovalResponse(
                        hold_id=hold_id,
                        approved=data.get("verdict") == "SEAL",
                        verdict=Verdict(data.get("verdict", "VOID")),
                        approved_by=data.get("approved_by"),
                        approved_at=data.get("approved_at"),
                        rejection_reason=data.get("rejection_reason"),
                    )

                # Check timeout
                if timeout:
                    elapsed = (datetime.utcnow() - start_time).total_seconds()
                    if elapsed > timeout:
                        raise HumanApprovalTimeoutError(
                            f"Timeout waiting for approval of {hold_id}"
                        )

                await asyncio.sleep(poll_interval)

            except httpx.HTTPError as e:
                raise GatewayConnectionError(f"Failed to poll hold status: {e}")

    async def seal_to_vault(
        self,
        session_id: str,
        verdict: str,
        payload: Dict[str, Any],
        query_summary: str,
        category: str = "sdk",
    ) -> Dict[str, Any]:
        """Seal operation result to VAULT999."""
        response = await self._client.post(
            "/vault/seal",
            json={
                "session_id": session_id,
                "verdict": verdict,
                "payload": payload,
                "query_summary": query_summary,
                "category": category,
            },
        )
        response.raise_for_status()
        return response.json()

    def create_session(
        self,
        actor_id: str,
        actor_type: str = "human",
        groups: Optional[List[str]] = None,
        team: Optional[str] = None,
    ) -> Session:
        """Create a new SDK session."""
        return Session(
            client=self,
            actor_id=actor_id,
            actor_type=ActorType(actor_type),
            groups=groups or [],
            team=team,
        )

    async def _notify_channels(
        self,
        request: HumanApprovalRequest,
        channels: List[str],
    ):
        """Send notifications to approval channels."""
        # Placeholder: actual implementation would integrate with
        # Slack webhooks, email SMTP, etc.
        pass

    def _parse_decision(
        self,
        data: Dict[str, Any],
        session_id: str,
        tool_name: str,
    ) -> GatewayDecision:
        """Parse gateway response into GatewayDecision."""
        from .types import FloorResult, BlastRadius

        floors = [
            FloorResult(
                floor=f.get("floor", "F?"),
                name=f.get("name", "Unknown"),
                passed=f.get("passed", False),
                score=f.get("score", 0.0),
                detail=f.get("detail"),
            )
            for f in data.get("floors", [])
        ]

        blast_data = data.get("blast_radius")
        blast = (
            BlastRadius(
                score=blast_data.get("score", 0.0),
                affected_pods=blast_data.get("affected_pods", 0),
                affected_deployments=blast_data.get("affected_deployments", 0),
                critical_namespaces=blast_data.get("critical_namespaces", []),
                mitigation_suggestions=blast_data.get("mitigations", []),
            )
            if blast_data
            else None
        )

        return GatewayDecision(
            session_id=session_id,
            tool_name=tool_name,
            tool_class=ToolClass(data.get("tool_class", "infra_write")),
            verdict=Verdict(data.get("verdict", "VOID")),
            floors=floors,
            hard_failures=data.get("hard_failures", []),
            blast_radius=blast,
            reasoning=data.get("reason", ""),
            manifest_hash=data.get("manifest_hash"),
            downstream_endpoint=data.get("downstream_endpoint"),
        )

    async def close(self):
        """Close client connection."""
        await self._client.aclose()


class Session:
    """
    High-level session interface for arifOS SDK.

    Encapsulates actor identity and provides convenient methods
    for constitutional operations.
    """

    def __init__(
        self,
        client: ArifOSClient,
        actor_id: str,
        actor_type: ActorType,
        groups: List[str],
        team: Optional[str] = None,
    ):
        self.client = client
        self.actor_id = actor_id
        self.actor_type = actor_type
        self.groups = groups
        self.team = team
        self.session_id = f"sdk-{uuid.uuid4().hex[:12]}"
        self._context = SessionContext(
            session_id=self.session_id,
            actor_id=actor_id,
            actor_type=actor_type,
            groups=groups,
            team=team,
        )

    async def check_action(
        self,
        tool: str,
        payload: Dict[str, Any],
    ) -> GatewayDecision:
        """Check action constitutionally."""
        return await self.client.check_action(
            tool_name=tool,
            payload=payload,
            session_id=self.session_id,
            actor_id=self.actor_id,
        )

    async def apply_manifest(
        self,
        manifest: str,
        namespace: str,
        strategy: str = "rolling",
        dry_run: bool = False,
    ) -> GatewayDecision:
        """
        Convenience method for K8s apply.

        Example:
            result = await session.apply_manifest(
                manifest="apiVersion: apps/v1...",
                namespace="prod",
                strategy="canary",
            )

            if result.requires_human_approval:
                approval = await session.request_approval(result)
                final = await session.await_approval(approval.hold_id)
        """
        return await self.check_action(
            tool="k8s_apply_guarded",
            payload={
                "manifest": manifest,
                "namespace": namespace,
                "strategy": strategy,
                "dry_run": dry_run,
            },
        )

    async def request_approval(
        self,
        decision: GatewayDecision,
        notify: Optional[List[str]] = None,
    ) -> HumanApprovalRequest:
        """Request human approval for 888_HOLD."""
        return await self.client.request_human_approval(decision, notify)

    async def await_approval(
        self,
        hold_id: str,
        timeout: Optional[float] = None,
    ) -> HumanApprovalResponse:
        """Wait for human approval."""
        return await self.client.await_human_approval(hold_id, timeout)

    async def seal(
        self,
        verdict: str,
        payload: Dict[str, Any],
        summary: str,
    ):
        """Seal to VAULT999."""
        return await self.client.seal_to_vault(
            session_id=self.session_id,
            verdict=verdict,
            payload=payload,
            query_summary=summary,
        )

    @property
    def accountable_human(self) -> str:
        """Get ultimately accountable human for this session."""
        return self._context.get_accountable_human()
