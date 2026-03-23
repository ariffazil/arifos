# arifOS Kernel Tool Blueprint for Agentic Systems

## Current arifOS surface used as source of truth

The live arifOS MCP deployment exposes an **M‑11 mega‑tool surface** (11 tools, 37 modes) and advertises it via the public `/tools` endpoint, alongside a health+capability map at `/health`. citeturn15view0turn14view1

The same `/health` document states the server is healthy, reports the **transport as `streamable-http`**, and publishes a **capability map that is intentionally redacted** (capabilities + credential classes, but not raw secrets). citeturn14view1

Governance in arifOS is defined as **13 constitutional floors** (hard/soft), a **000→999 metabolic loop**, and an explicit **888_HOLD** contract for high-stakes or ambiguous situations (e.g., destructive DB ops, production deploys, mass file changes, credential handling, force pushes). citeturn21view0

The repository’s agent contract reinforces the operational invariants most relevant for “agent kernel tools”: start sessions with `init_anchor`, carry `auth_context` forward, and treat “reality sensing” as mandatory grounding rather than trusting model weights for current state. citeturn10view1turn21view0

## Two-layer model aligned to arifOS canon

This blueprint treats the system as two distinct layers:

- **Layer A — Substrate capability classes (how state changes in digital reality):** Inspect, Read, Recall, Write, Update, Delete, Execute, Commit, Communicate. (These are the “action surface” primitives you referenced.)
- **Layer B — Kernel organs (how governed agency works above the action surface):** the **000→999 loop**, floors, verdicts, and the 888_HOLD escalation contract. citeturn21view0turn10view1

Crucially, arifOS defines which floors are **HARD (VOID on fail)** vs **SOFT (SABAR on fail)**, and ties irreversible/high-stakes actions to **888_HOLD** and **human sovereignty**. citeturn21view0

## Canonical YAML blueprint

The YAML block below is a **two-layer tool matrix** (tool → modes → substrate class invoked + kernel organ governing that call), plus a **HOLD‑prone risk band** (Delete/Execute/Commit/Communicate), and a **floor gating policy** keyed off the canonical floor definitions and 888_HOLD triggers. citeturn21view0turn15view0turn14view1turn10view1

```yaml
arifOS_kernel_tools_blueprint:
  blueprint_version: "2026-03-24"
  observed_runtime:
    server:
      version: "2026.03.22"
      transport: "streamable-http"
      tool_surface:
        mega_tools: 11
        total_modes_loaded: 37
      endpoints:
        health: "https://arifosmcp.arif-fazil.com/health"
        tools:  "https://arifosmcp.arif-fazil.com/tools"
        mcp:    "https://arifosmcp.arif-fazil.com/mcp"
    notes:
      - "Capability map reports capabilities and credential classes; it must not reveal raw secrets."
      - "All mega-tools share a common envelope: session_id, auth_context, risk_tier, dry_run, allow_execution."

  layer_A_substrate_capability_classes:
    # What changes in digital reality (or its governed substrate: tokens, vault entries, vector memory, filesystem, network calls)
    classes:
      inspect:
        delta_s_band: "reversible"
        definition: "Structure-only observation: list/metadata/status without ingesting full content."
      read:
        delta_s_band: "reversible"
        definition: "Content retrieval with no state mutation."
      recall:
        delta_s_band: "reversible"
        definition: "Memory retrieval (semantic or exact) without mutation."
      write:
        delta_s_band: "mutable"
        definition: "Create new state (new file, new memory entry, new evidence node)."
      update:
        delta_s_band: "mutable"
        definition: "Modify existing state in-place (patch, rename, alter config)."
      delete:
        delta_s_band: "irreversible"
        definition: "Remove state (delete/purge/drop). Treat as irreversible unless proven reversible."
      execute:
        delta_s_band: "irreversible"
        definition: "Run code or commands with potentially unbounded side effects."
      commit:
        delta_s_band: "irreversible"
        definition: "Atomic external finalize: push, deploy, ledger seal, irreversible write to audit chain."
      communicate:
        delta_s_band: "irreversible"
        definition: "External signaling (webhook, notification, cross-agent message) that creates downstream effects."

    hold_prone_classes:
      # Policy: these must be explicitly highlighted as escalation-likely
      - delete
      - execute
      - commit
      - communicate

  layer_B_kernel_organs:
    # Governed runtime roles above the substrate actions (stage-coded)
    organs:
      anchor_000:
        stage: "000_INIT"
        role: "Identity binding, authority gating, injection scan entrypoint, session trust chain."
      sense_111:
        stage: "111_SENSE"
        role: "Reality acquisition + evidence ingestion routes; intent classification and lane assignment."
      reason_333:
        stage: "333_MIND"
        role: "First-principles reasoning, decomposition, self-reflection prior to action."
      router_444:
        stage: "444_ROUTER"
        role: "Metabolic conductor: routes across organs, risk tiers, and execution enablement."
      memory_555:
        stage: "555_MEMORY"
        role: "Episodic/semantic store, retrieve, forget; engineering memory as governed working set."
      heart_666:
        stage: "666_HEART"
        role: "Ethics, stakeholder impact modeling, critique/simulate loop for consequences."
      judge_888:
        stage: "888_JUDGE"
        role: "Verdict issuance, defense posture, HOLD/VOID adjudication, final gate before sealing."
      seal_999:
        stage: "999_VAULT"
        role: "Immutable commit + integrity verification of the vault chain."

  constitutional_floors_policy:
    # Canon class: Hard floors VOID; Soft floors SABAR; HOLD when high-stakes triggers exist.
    floors:
      hard_void_on_fail: [F1, F2, F10, F11, F12, F13]
      soft_sabar_on_fail: [F3, F4, F5, F6, F7, F8, F9]

    baseline_gating_by_substrate_class:
      inspect:
        must_check: [F11, F12]
        should_check: [F4]
      read:
        must_check: [F2, F11, F12]
        should_check: [F3, F4]
      recall:
        must_check: [F2, F11, F12]
        should_check: [F3, F4, F7]
      write:
        must_check: [F1, F11, F12]
        should_check: [F4, F5, F7, F9]
      update:
        must_check: [F1, F11, F12]
        should_check: [F4, F5, F7, F9, F10]
      delete:
        must_check: [F1, F11, F12, F13]
        should_check: [F2, F4, F5, F7]
        escalation: "888_HOLD default unless cryptographically reversible + explicitly approved"
      execute:
        must_check: [F1, F11, F12, F13]
        should_check: [F2, F4, F5, F6, F7, F9]
        escalation: "888_HOLD default unless bounded sandbox + explicit allow_execution"
      commit:
        must_check: [F1, F11, F12]
        should_check: [F3, F4, F5, F7, F13]
        escalation: "888_HOLD when commit affects production, history, or irreversible external systems"
      communicate:
        must_check: [F11, F12, F13]
        should_check: [F2, F4, F5, F6, F9]
        escalation: "888_HOLD when notifying external actors/systems outside declared scope"

    888_hold_triggers_non_exhaustive:
      # Directly aligned with the governance contract
      - "database: DROP/TRUNCATE/DELETE without WHERE"
      - "production deployments"
      - "mass file changes (>10 files)"
      - "credential or secret handling"
      - "git history modification (rebase/force push)"
      - "user correction of constitutional claim"
      - "conflicting evidence sources across tiers"

  mcp_tool_surface_M11:
    # Canonical live mega-tools (names, stages, lanes, and modes)
    # Each mode maps to: substrate class invoked + organ governing, plus HOLD-prone flag.
    tools:
      init_anchor:
        stage: "000_INIT"
        lane: "PSI"
        organ_governing: "anchor_000"
        modes:
          init:
            substrate_invokes: [write, commit]
            hold_prone: false
            default_risk_tier: "low"
            policy_notes:
              - "Bind session identity; mint/refresh authority context; establish trust chain."
          state:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "low"
          status:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "low"
          refresh:
            substrate_invokes: [update, commit]
            hold_prone: false
            default_risk_tier: "medium"
            policy_notes:
              - "Rotate/refresh tokens; treat as commit-like because it changes authority state."
          revoke:
            substrate_invokes: [delete]
            hold_prone: true
            default_risk_tier: "high"
            policy_notes:
              - "Kill session / revoke authority; treat as destructive regardless of convenience."

      physics_reality:
        stage: "111_SENSE"
        lane: "DELTA"
        organ_governing: "sense_111"
        modes:
          search:
            substrate_invokes: [read]
            hold_prone: false
            default_risk_tier: "medium"
          ingest:
            substrate_invokes: [read, write]
            hold_prone: false
            default_risk_tier: "medium"
            policy_notes:
              - "Ingest implies state creation (evidence bundle, vector/evidence node)."
          compass:
            substrate_invokes: [inspect, read]
            hold_prone: false
            default_risk_tier: "medium"
          atlas:
            substrate_invokes: [write, update]
            hold_prone: false
            default_risk_tier: "medium"
          time:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "low"

      agi_mind:
        stage: "333_MIND"
        lane: "DELTA"
        organ_governing: "reason_333"
        modes:
          reason:
            substrate_invokes: []
            hold_prone: false
            default_risk_tier: "medium"
            policy_notes:
              - "Cognitive-only; outputs plans/proposals, not side effects."
          reflect:
            substrate_invokes: []
            hold_prone: false
            default_risk_tier: "medium"
            policy_notes:
              - "Self-audit; should elevate uncertainty band when evidence is weak."
          forge:
            substrate_invokes: [write]
            hold_prone: false
            default_risk_tier: "medium"
            policy_notes:
              - "Forge here means synthesize artifacts (patch drafts/spec), not execute by default."

      asi_heart:
        stage: "666_HEART"
        lane: "OMEGA"
        organ_governing: "heart_666"
        modes:
          critique:
            substrate_invokes: []
            hold_prone: false
            default_risk_tier: "medium"
          simulate:
            substrate_invokes: []
            hold_prone: false
            default_risk_tier: "medium"

      engineering_memory:
        stage: "555_MEMORY"
        lane: "OMEGA"
        organ_governing: "memory_555"
        modes:
          vector_query:
            substrate_invokes: [recall]
            hold_prone: false
            default_risk_tier: "medium"
          vector_store:
            substrate_invokes: [write]
            hold_prone: false
            default_risk_tier: "medium"
          vector_forget:
            substrate_invokes: [delete]
            hold_prone: true
            default_risk_tier: "high"
            policy_notes:
              - "Forget is deletion; require explicit intent scope + authority."
          generate:
            substrate_invokes: [write]
            hold_prone: false
            default_risk_tier: "medium"
          engineer:
            substrate_invokes: [execute, write, update, commit]
            hold_prone: true
            default_risk_tier: "high"
            policy_notes:
              - "This is a high-blast-radius mode: treat as EXECUTE + COMMIT until proven sandboxed."

      code_engine:
        stage: "M-3_EXEC"
        lane: "ALL"
        organ_governing: "router_444"
        modes:
          fs:
            substrate_invokes: [inspect, read]
            hold_prone: false
            default_risk_tier: "medium"
          process:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "medium"
          net:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "medium"
          tail:
            substrate_invokes: [read]
            hold_prone: false
            default_risk_tier: "medium"
          replay:
            substrate_invokes: [recall, inspect]
            hold_prone: false
            default_risk_tier: "medium"

      math_estimator:
        stage: "444_ROUTER"
        lane: "DELTA"
        organ_governing: "router_444"
        modes:
          cost:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "medium"
          health:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "medium"
          vitals:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "medium"

      architect_registry:
        stage: "M-4_ARCH"
        lane: "DELTA"
        organ_governing: "router_444"
        modes:
          list:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "medium"
          read:
            substrate_invokes: [read]
            hold_prone: false
            default_risk_tier: "medium"
          register:
            substrate_invokes: [write, update, commit]
            hold_prone: true
            default_risk_tier: "high"
            policy_notes:
              - "Registry changes are effectively configuration commits; HOLD-prone in production."

      arifOS_kernel:
        stage: "444_ROUTER"
        lane: "DELTA/PSI"
        organ_governing: "router_444"
        modes:
          kernel:
            substrate_invokes: ["meta:may_invoke_any"]
            hold_prone: true
            default_risk_tier: "medium"
            policy_notes:
              - "Conductor: traverses multiple stages; execution depends on allow_execution + verdict."
          status:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "low"

      apex_soul:
        stage: "888_JUDGE"
        lane: "PSI"
        organ_governing: "judge_888"
        modes:
          rules:
            substrate_invokes: [read, inspect]
            hold_prone: false
            default_risk_tier: "medium"
          judge:
            substrate_invokes: []
            hold_prone: false
            default_risk_tier: "medium"
          validate:
            substrate_invokes: []
            hold_prone: false
            default_risk_tier: "medium"
          hold:
            substrate_invokes: []
            hold_prone: false
            default_risk_tier: "high"
          armor:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "high"
          probe:
            substrate_invokes: [inspect]
            hold_prone: false
            default_risk_tier: "medium"
          notify:
            substrate_invokes: [communicate]
            hold_prone: true
            default_risk_tier: "high"
            policy_notes:
              - "External notifications must respect scope + sovereignty; default to HOLD if ambiguous."

      vault_ledger:
        stage: "999_VAULT"
        lane: "PSI"
        organ_governing: "seal_999"
        modes:
          verify:
            substrate_invokes: [inspect, read]
            hold_prone: false
            default_risk_tier: "medium"
          seal:
            substrate_invokes: [commit]
            hold_prone: true
            default_risk_tier: "high"
            policy_notes:
              - "Seal is the canonical immutable commit; treat as COMMIT and require strict authority."

  invariants_for_any_agent_embedding:
    # This is the "kernel tools must exist" statement, in arifOS terms.
    minimal_kernel_primitives_required:
      - "anchor_000: session identity + authority"
      - "sense_111: reality grounding"
      - "reason_333: plan + self-audit"
      - "memory_555: continuity store/retrieve/forget"
      - "heart_666: critique + simulate consequences"
      - "judge_888: verdicts + HOLD/VOID"
      - "seal_999: immutable audit"
    substrate_minimum_required:
      - inspect
      - read
      - recall
      - write
      - update
      - delete
      - execute
      - commit
      - communicate
```

## MCP and Web MCP shipping blueprint aligned to arifOS

MCP is a JSON‑RPC based protocol with two standard transports: **stdio** and **Streamable HTTP**. citeturn2view5  
arifOS explicitly advertises multiple transports as available (`stdio`, `http`, `streamable-http`) and notes SSE deprecation in its FastMCP manifest. citeturn8view0

The repo also includes an MCP server manifest (`server.json`) that declares a **`streamable-http` remote** pointing at the `/mcp` endpoint. citeturn8view1

The arifOS integration guide shows the canonical JSON‑RPC methods used by clients (`tools/list`, `tools/call`) when speaking to `/mcp` over HTTP. citeturn7view0

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["Model Context Protocol diagram host client server tools resources prompts","Streamable HTTP MCP sequence diagram","Agent2Agent A2A protocol agent card diagram"],"num_per_query":1}

```yaml
shipping_blueprint:
  mcp:
    protocol: "jsonrpc-2.0"
    transports:
      stdio:
        use_for: ["local IDE agents", "dev sandbox", "tight trust boundary"]
        spec_notes:
          - "Newline-delimited JSON-RPC messages; stdout must contain only valid MCP messages."
      streamable_http:
        use_for: ["remote clients", "web deployments", "multi-client server"]
        endpoint_path: "/mcp"
        arifos_remote_example: "https://arifosmcp.arif-fazil.com/mcp"

    discovery_and_calls:
      list_tools_method: "tools/list"
      call_tool_method: "tools/call"
      required_envelope_fields:
        - session_id
        - auth_context
        - risk_tier
        - dry_run
        - allow_execution
      recommended_fields:
        - request_id
        - timestamp
        - debug

    manifests:
      # arifOS already ships both patterns
      modelcontextprotocol_server_json:
        schema: "https://static.modelcontextprotocol.io/schemas/2025-10-17/server.schema.json"
        file: "server.json"
        key_fields: ["name", "version", "remotes[type=streamable-http,url]"]
      fastmcp_manifest:
        schema: "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json"
        file: "fastmcp.json"
        key_fields: ["source.path", "deployment.transports_available", "authentication.header"]

    authn_authz_minimum:
      # Aligns to floors: F11 authority + F12 injection defense + F13 sovereignty
      http_header_api_key:
        header: "X-API-Key"
        mode: "optional for dev; mandatory for production"
      scope_rules:
        - "bind actor_id at init_anchor"
        - "deny tool mode outside declared intent scope"
        - "require explicit human approval for HOLD-prone substrate classes when risk_tier >= high"
```

## A2A shipping blueprint aligned to arifOS

A2A is designed for **agent‑to‑agent communication** and is explicitly positioned as complementary to MCP (agent‑to‑tool communication). citeturn2view6turn2view7

The A2A spec defines:
- standard discovery of an agent via **`/.well-known/agent-card.json`** (must return an AgentCard object), citeturn12view3  
- JSON‑RPC request shape for **`SendMessage`**, citeturn12view2  
- and optional AgentCard signing via **JWS** with canonicalization via **RFC 8785 (JCS)**. citeturn12view4

```yaml
shipping_blueprint:
  a2a:
    role: "arifOS_governance_agent"
    discovery:
      well_known_agent_card_path: "/.well-known/agent-card.json"
      signing:
        enabled_recommended: true
        method: "JWS"
        canonicalization: "RFC8785_JCS"
        key_rotation: "supported"

    rpc_binding:
      protocol: "jsonrpc-2.0"
      primary_methods:
        - SendMessage

    interop_with_mcp:
      pattern: "A2A_frontdoor -> arifOS_kernel (MCP) -> floor_verdict -> vault_seal"
      rationale:
        - "A2A keeps agent internals opaque; MCP remains the tool-call substrate behind the agent boundary."
        - "arifOS floors + 888_HOLD govern whether agent requests can proceed to tool execution."

    advertised_skills_minimum:
      # Skills are intentionally higher-level than substrate actions.
      # They map to kernel organs above the substrate.
      - name: "anchor_session"
        maps_to_organs: ["anchor_000"]
        description: "Initialize or resume governed identity + authorization context."
      - name: "ground_claims"
        maps_to_organs: ["sense_111"]
        description: "Ground assertions in external evidence; return evidence bundle + uncertainty."
      - name: "plan_and_decompose"
        maps_to_organs: ["reason_333", "memory_555"]
        description: "Turn a task into a bounded plan with explicit tool calls + rollback notes."
      - name: "simulate_and_critique"
        maps_to_organs: ["heart_666"]
        description: "Run consequence simulation and adversarial critique before any action."
      - name: "judge_and_gate"
        maps_to_organs: ["judge_888"]
        description: "Issue verdict; apply HOLD/VOID rules; require human confirmation when triggered."
      - name: "seal_audit"
        maps_to_organs: ["seal_999"]
        description: "Commit audit record to immutable ledger; provide verification handle."

    enforcement_notes:
      hold_prone_request_types:
        - "delete/execute/commit/communicate equivalents"
        - "production deployments"
        - "credential handling"
        - "mass changes"
      expected_behavior_on_hold:
        - "return HOLD with trigger type"
        - "provide a minimal human-readable decision packet"
        - "wait for explicit human approval token before continuing"
```

