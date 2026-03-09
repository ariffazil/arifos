# arifOS Tool Surface (Layered)

This repository exposes tools in two layers:

- Public interface (ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt) for external clients.
- Internal core (ARIFOS_PUBLIC_TOOL_PROFILE=full) for staged constitutional execution.

## Public Interface Tools (7)

1. metabolic_loop_router - one-call governed 000->999 execution.
2. search_reality - external grounding/search.
3. ingest_evidence - read evidence from URL source.
4. audit_rules - read-only governance/floor audit.
5. check_vital - read-only system health snapshot.
6. trace_replay - read-only replay of sealed trace telemetry.
7. open_apex_dashboard - launch APEX dashboard MCP app.

## Internal Core Stack (10)

1. init_anchor_state (000)
2. integrate_analyze_reflect (111)
3. reason_mind_synthesis (333)
4. metabolic_loop_router (444)
5. vector_memory_store (555)
6. assess_heart_impact (666A)
7. critique_thought_audit (666B)
8. quantum_eureka_forge (777)
9. apex_judge_verdict (888)
10. seal_vault_commit (999)

## Embedded Reality Stage

Inside metabolic_loop_router, arifOS applies an explicit 222_REALITY verification stage between 333_MIND and 666_HEART.

- It is risk-tier aware (ARIFOS_REALITY_REQUIRED_TIERS, default A,B).
- It feeds grounding status/score into judge synthesis.
- It is sealed into vault telemetry and retrievable via trace_replay.
