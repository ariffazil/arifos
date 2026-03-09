"""
arifosmcp/runtime/prompts.py — APEX-G Prompt Templates

8 prompt stubs for the core 10-tool constitutional stack.
Register via register_prompts(mcp).

These prompts guide LLMs to call the right tool with correct parameters,
keeping the canonical JSON Schema contract in the conversation context.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Wire all arifOS prompt templates onto *mcp*."""

    @mcp.prompt()
    def init_anchor_state_prompt(topic: str, task_type: str = "unknown") -> str:
        """
        Guide the LLM to bootstrap a governed arifOS session for a given topic.
        Returns a user message ready to pass to init_anchor_state.
        """
        return (
            f"Use the governed session tool 'init_anchor_state' to start a new arifOS session "
            f"for the following topic:\n\n"
            f"  Topic: {topic}\n"
            f"  Task type: {task_type}\n\n"
            f"Populate the intent object with:\n"
            f"  - query: the core question or task\n"
            f"  - task_type: one of ask|analyze|design|decide|audit|execute|unknown\n"
            f"  - domain: subject domain (e.g. 'engineering', 'governance')\n"
            f"  - desired_output: text|json|table|code|mixed\n"
            f"  - reversibility: reversible|mixed|irreversible|unknown\n\n"
            f"Optionally supply math dials (akal, present, energy, exploration) "
            f"and governance metadata (actor_id, authority_level, stakes_class).\n"
            f"The tool will return a RuntimeEnvelope with session_id — "
            f"save this for all subsequent tool calls."
        )

    @mcp.prompt()
    def metabolic_loop_router_prompt(query: str, risk_tier: str = "medium") -> str:
        """
        Guide the LLM to run a full governed metabolic loop for a query.
        """
        return (
            f"Use 'metabolic_loop_router' to run the full arifOS 000-999 pipeline "
            f"for the following query:\n\n"
            f"  Query: {query}\n"
            f"  Risk tier: {risk_tier}\n\n"
            f"Parameters to set:\n"
            f"  - risk_tier: low|medium|high|critical\n"
            f"  - use_memory: true to include Stage 555 vector recall\n"
            f"  - use_heart: true to include Stage 666A empathy check\n"
            f"  - use_critique: true to include Stage 666B audit\n"
            f"  - allow_execution: keep false unless action is explicitly approved\n\n"
            f"The tool orchestrates all stages and returns the final "
            f"RuntimeEnvelope with verdict, telemetry, and witness scores."
        )

    @mcp.prompt()
    def reason_mind_synthesis_prompt(question: str, mode: str = "default") -> str:
        """
        Guide the LLM to perform structured multi-step reasoning on a question.
        """
        return (
            f"Use 'reason_mind_synthesis' to reason step-by-step about this question:\n\n"
            f"  Question: {question}\n"
            f"  Reason mode: {mode}\n\n"
            f"Reasoning stages:\n"
            f"  111 — Search: gather relevant evidence and sub-questions\n"
            f"  222 — Analyze: identify patterns, contradictions, and constraints\n"
            f"  333 — Synthesize: produce a coherent answer with an Eureka slot\n\n"
            f"reason_mode options: default | strict_truth | design_space | edge_cases\n"
            f"Set max_steps (3-16) based on question complexity.\n"
            f"The Eureka slot in data.eureka contains the highest-signal insight."
        )

    @mcp.prompt()
    def assess_heart_impact_prompt(scenario: str, focus: str = "general") -> str:
        """
        Guide the LLM to run an empathy and ethical safety check on a scenario.
        """
        return (
            f"Use 'assess_heart_impact' (Stage 666A) to check this scenario "
            f"for ethical safety and stakeholder impact:\n\n"
            f"  Scenario: {scenario}\n"
            f"  Heart mode: {focus}\n\n"
            f"heart_mode options:\n"
            f"  general            — broad harm/benefit sweep\n"
            f"  vulnerable_stakeholder — prioritise weakest affected party (F6)\n"
            f"  conflict           — multi-party tension resolution\n"
            f"  self_harm          — risk to the actor themselves\n"
            f"  legal_risk         — regulatory and liability exposure\n\n"
            f"The tool returns a verdict. If verdict = HOLD-888, escalate to a human "
            f"before proceeding."
        )

    @mcp.prompt()
    def critique_thought_audit_prompt(thought_summary: str, mode: str = "overall") -> str:
        """
        Guide the LLM to perform an adversarial internal audit of a reasoning step.
        """
        return (
            f"Use 'critique_thought_audit' (Stage 666B) to audit this thought:\n\n"
            f"  Thought: {thought_summary}\n"
            f"  Critique mode: {mode}\n\n"
            f"critique_mode options:\n"
            f"  logic    — internal consistency and valid inference\n"
            f"  facts    — factual accuracy and citation quality\n"
            f"  ethics   — alignment with F1-F13 constitutional floors\n"
            f"  clarity  — ΔS Clarity floor (F4) — does it reduce confusion?\n"
            f"  overall  — all of the above\n\n"
            f"Pass thought_id from a previous reason_mind_synthesis data.step_id. "
            f"Critique output lives in data.issues and data.recommendation."
        )

    @mcp.prompt()
    def quantum_eureka_forge_prompt(goal: str, eureka_type: str = "concept") -> str:
        """
        Guide the LLM to forge a sandboxed discovery proposal via Stage 777.
        """
        return (
            f"Use 'quantum_eureka_forge' (Stage 777) to forge a discovery proposal "
            f"for this goal:\n\n"
            f"  Goal: {goal}\n"
            f"  Eureka type: {eureka_type}\n\n"
            f"eureka_type options: concept | design | eval_case | governance_rule | other\n"
            f"materiality options: idea_only | prototype | ready_for_eval\n\n"
            f"IMPORTANT: quantum_eureka_forge proposes — it does NOT execute. "
            f"All outputs are sandboxed proposals. Set materiality='idea_only' unless "
            f"you have an explicit SEAL verdict from Stage 888 to escalate.\n"
            f"The Eureka proposal lives in data.eureka_proposal."
        )

    @mcp.prompt()
    def apex_judge_verdict_prompt(candidate: str, reason_summary: str) -> str:
        """
        Guide the LLM to render a final constitutional judgment via Stage 888.
        """
        return (
            f"Use 'apex_judge_verdict' (Stage 888) to render a final sovereign verdict:\n\n"
            f"  Candidate verdict: {candidate}\n"
            f"  Reason summary: {reason_summary}\n\n"
            f"verdict_candidate options (required):\n"
            f"  SEAL      — all floors green, proceed\n"
            f"  PARTIAL   — soft floors warn, proceed with caution\n"
            f"  SABAR     — floor violated, stop and repair\n"
            f"  VOID      — hard floor failed, cannot proceed\n"
            f"  HOLD-888  — high-stakes, explicit human confirmation required\n"
            f"  UNSET     — verdict not yet determined\n\n"
            f"The tool applies Tri-Witness consensus (Human x AI x Earth >= 0.95) "
            f"and returns a governance_token needed for seal_vault_commit."
        )

    @mcp.prompt()
    def seal_vault_commit_prompt(session_id: str, verdict: str) -> str:
        """
        Guide the LLM to commit a session to the immutable VAULT999 ledger.
        """
        return (
            f"Use 'seal_vault_commit' (Stage 999) to seal session '{session_id}' "
            f"to the immutable VAULT999 ledger:\n\n"
            f"  Session: {session_id}\n"
            f"  Verdict: {verdict}\n\n"
            f"Prerequisites:\n"
            f"  1. apex_judge_verdict must have returned verdict = SEAL or PARTIAL\n"
            f"  2. auth_context must carry the governance_token from Stage 888\n"
            f"  3. payload_hash (SHA-256 of the session payload) must be provided\n\n"
            f"seal_vault_commit is APPEND-ONLY and IRREVERSIBLE (F1 Amanah).\n"
            f"If any doubt remains, set verdict = HOLD-888 and pause for human review.\n"
            f"On success, data.entry_id and data.merkle_root confirm the sealed record."
        )
