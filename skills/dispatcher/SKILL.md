# Skill: Dispatcher (Governance-Compliant Routing)

## Description
This skill enables the "Dispatcher Mode" where the agent delegates tasks to specific models based on a strict `routing.json` policy, rather than random heuristics. It ensures F1/F2 compliance by logging every decision.

## Usage

When a user gives a complex task or explicitly asks for "Dispatch" or "Orchestrate":

1.  **Read Policy:** Load `/root/.openclaw/workspace/routing.json`.
2.  **Classify Task:** Match user input against `keywords` in the JSON.
    *   If ambiguous, default to `default_model`.
3.  **Log Decision:** Append a line to `/root/.openclaw/workspace/routing_ledger.md`.
4.  **Execute (Spawn):** Use `sessions_spawn` (or simulation) to call the target model.
5.  **Synthesize:** Combine results if multiple models were used.

## Logic (Pseudo-Code)

```python
def route_task(user_prompt):
    policy = load_json("routing.json")
    
    # 1. Classify
    selected_route = None
    for route in policy["routes"]:
        if any(keyword in user_prompt.lower() for keyword in route["keywords"]):
            selected_route = route
            break
    
    if not selected_route:
        model = policy["default_model"]
        task_type = "unknown_default"
        reason = "No keyword match; using generalist."
    else:
        model = selected_route["primary"]
        task_type = selected_route["task_type"]
        reason = selected_route["reason"]

    # 2. Log
    log_entry = f"[{timestamp}] | TASK: {task_type} | MODEL: {model} | REASON: {reason}"
    append_to_file("routing_ledger.md", log_entry)

    # 3. Return Model Config
    return model, task_type
```

## Governance Rules (The 13 Floors)
*   **No Black Box:** You must explain *why* a model was chosen (cite the route reason).
*   **No Hidden Overrides:** Do not deviate from `routing.json` unless the user explicitly overrides.
*   **Audit First:** Log before executing.
