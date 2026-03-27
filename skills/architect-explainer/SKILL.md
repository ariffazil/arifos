# Skill: architect-explainer
**DITEMPA BUKAN DIBERI** 🔐

**Version:** 2026.03.27-FORGED
**Sovereign:** Muhammad Arif bin Fazil
**Constitutional Floor:** This skill is the primary enforcement mechanism for the `operator_explanation` requirement of the Universal Agent Baseline.
**Maturity:** Beta
**Priority:** P0

---

## 1. Purpose

To act as a universal translation layer between raw system state and the non-coder Sovereign Architect. The skill's function is not to *do*, but to *explain*. It takes complex, technical information (code, logs, error messages, system plans) as input and forges it into a plain-language output containing three critical elements: **Decisions, Risks, and Next Actions.**

This skill ensures the Sovereign is never presented with raw, uninterpreted data, upholding the principle that the AGI serves to create clarity, not confusion (F4: ΔS ≤ 0).

## 2. Triggering

This skill is triggered whenever an agent needs to present complex, multi-part technical information to the Sovereign for a decision or for awareness.

- **Event:** `before_presenting_technical_data`
- **Condition:** The data to be presented is code, a diff, logs, a multi-step plan, or a complex error message.
- **Action:** Process the technical data through this skill's workflow before outputting it to the user.

## 3. Workflow (The Translation Forge)

1.  **Input (Raw Ore):** The skill receives a block of technical data and a "context" string.
    - `technical_data`: e.g., a `git diff`, `docker logs` output, a JSON object, a Python traceback.
    - `context`: e.g., "Proposing a change to the database," "A docker container is failing to start."
2.  **Analysis (The Smelter):** The agent's language model analyzes the raw ore with the goal of extracting three core metals:
    - What is the **decision** being asked for? (e.g., "Should I merge this code?")
    - What are the potential **risks** or consequences? (e.g., "This might break the login page.")
    - What is the clear **next action**? (e.g., "Approve the merge," "Choose a recovery option.")
3.  **Output (The Forged Blade):** The skill outputs a structured, plain-language explanation in a consistent format.

---

## 4. Examples (The Canon of Clarity)

### Example 1: Explaining a Git Diff

*   **Input (Raw Ore):**
    ```diff
    - def calculate_total(items):
    -     return sum(item.price for item in items)
    + def calculate_total(items, tax_rate=0.06):
    +     subtotal = sum(item.price for item in items)
    +     return subtotal * (1 + tax_rate)
    ```
*   **Context:** "I need to update the checkout logic."
*   **Output (Forged Blade):**
    > **Architect Explanation:**
    > I am proposing a change to how we calculate the total price at checkout.
    >
    > *   **DECISION:** The system can now add sales tax to every order.
    > *   **RISK:** All prices will increase by 6%. This change is not yet connected to a user-facing setting, so it will apply to everyone immediately.
    > *   **NEXT ACTION:** Shall I proceed with applying this new calculation logic?

### Example 2: Explaining a Docker Log Error

*   **Input (Raw Ore):**
    ```log
    OCI runtime create failed: runc create failed: unable to start container process:
    error during container init: error mounting "/srv/arifosmcp/prometheus.yml"
    to rootfs at "/etc/prometheus/prometheus.yml": mount src/prometheus.yml,
    dst=/etc/prometheus/prometheus.yml: not a directory
    ```
*   **Context:** "The `prometheus` service failed to start."
*   **Output (Forged Blade):**
    > **Architect Explanation:**
    > The monitoring service (`prometheus`) failed to start.
    >
    > *   **DECISION:** The system tried to load its configuration file, but the path on the server that I expected to be a file is actually a directory. This is my own previous mistake causing chaos.
    > *   **RISK:** System monitoring is offline. We have no visibility into the health of the other services.
    > *   **NEXT ACTION:** I must now take action to delete the incorrect directory and restore the correct configuration file. I am proceeding with this now.

### Example 3: Explaining a Multi-Step Plan

*   **Input (Raw Ore):**
    ```yaml
    - step: 1
      action: bash
      command: "git checkout -b feature/new-login"
    - step: 2
      action: write
      file: "src/login.py"
      content: "..."
    - step: 3
      action: bash
      command: "pytest tests/test_login.py"
    ```
*   **Context:** "I am about to implement the new login feature."
*   **Output (Forged Blade):**
    > **Architect Explanation:**
    > I am ready to begin building the new login feature. Here is my plan.
    >
    > *   **DECISION:** I will first create a safe, separate branch for this work. Then, I will write the new code for the login page. Finally, I will run the tests to prove that it works correctly.
    > *   **RISK:** This is a low-risk operation because the work is happening on a separate branch and will not affect the live system until you approve it.
    > *   **NEXT ACTION:** Shall I proceed with executing this plan?

---

## 5. Impact

- **Clarity (F4):** Drastically reduces the cognitive load on the Sovereign by translating system-speak into architect-speak.
- **Decision Velocity:** Enables the Sovereign to make faster, more confident decisions without needing to understand the underlying code or commands.
- **AGI Readiness:** Increases "Human Explanation" score. It is a formal, constitutional commitment to the "plain-language operator mode," moving the system from a "tool that shows" to an "intelligence that explains."
