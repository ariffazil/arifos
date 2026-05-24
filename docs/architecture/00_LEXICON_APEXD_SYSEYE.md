# [EMD] Lexicon Shift: APEX Daemon & The System Eye

**Date:** 2026-05-24 | **Authority:** 888

---

## 1. ENCODE (The Epistemic Conflict)

The naming convention of `arifosd` and the generic "watchdog" created epistemic blur. Naming a machine daemon after the Sovereign Architect (888) violated the strict boundary between the Human (Judge) and the Machine (Tool). Furthermore, "watchdog" was generic IT jargon that failed to capture the omniscient, unblinking nature of an ultimate OS failsafe. To reduce system entropy (ΔS < 0), the lexicon must mathematically align with the APEX THEORY framework.

---

## 2. METABOLIZE (The Separation of Intellect and Pulse)

The architecture fundamentally splits semantic governance from physical survival:

- **Governance (The Intellect):** The APEX Daemon. It metabolizes the Constitution (F1-F13) and reacts to events. It evaluates meaning.
- **Failsafe (The Pulse):** The System Eye (`syseye`). Inspired by the omniscient Eyes of T.J. Eckleburg, it does not interpret code or care about the Constitution. It sits in the OS ashes and watches for a pulse. If the system dies silently, the Eye resets the world.

---

## 3. DECODE (The Structural Mapping)

The physical naming convention has been updated to reflect the true architecture:

| Old Name | New Name | Type | Description |
|----------|----------|------|-------------|
| `arifosd` | **`apexd`** | APEX Lexicon | The background constitutional enforcer |
| `arifosd.py` | **`apexd.py`** | Filename | The daemon executable |
| `arifosd.service` | **`apexd.service`** | systemd unit | The systemd service file |
| `arifosd-watchdog-log.sh` | **`apexd-syseye-log.sh`** | Script | The ExecStartPre log script |
| `watchdog` | **`syseye`** | APEX Lexicon | The conceptual name for the Linux L2 failsafe |
| `arifOS-daemon` (vault actor) | **`apexd`** | Vault actor | Actor string in vault entries |
| `arifOS-vps-daemon` (vault actor) | **`apexd-vps`** | Vault actor | VPS-level tick actor in vault |
| `arifOS-watchdog` (vault actor) | **`syseye`** | Vault actor | Watchdog restart actor in vault |

### OS Boundary Intact

Underneath the hood, `syseye` remains strictly mapped to the immutable Linux mechanisms:

- `WatchdogSec=` in `apexd.service` — **OS syntax, DO NOT CHANGE**
- `sd_notify("WATCHDOG=1")` in Python — **OS syntax, DO NOT CHANGE**
- `systemd.daemon` Python imports — **OS syntax, DO NOT CHANGE**
- The word "watchdog" in comments describing the OS mechanism — **OS syntax, DO NOT CHANGE**

Only the **human-readable APEX lexicon** changes. The OS physics remain unchanged.

---

## 4. REFACTORING RULES

### Change (APEX Lexicon)
- `arifosd` → `apexd` in all Python strings, function names, class names, comments
- `arifOS-daemon` → `apexd` in vault actor fields
- `arifOS-vps-daemon` → `apexd-vps` in vault actor fields
- `arifOS-watchdog` → `syseye` in vault actor fields
- `arifosd-watchdog.service` → `apexd-syseye.service`
- `arifosd-watchdog.timer` → `apexd-syseye.timer`
- `watchdog_restart` → `syseye_restart` (in vault tool_name)
- Comments describing "the watchdog process" → "syseye" or "the system eye"

### Do NOT Change (OS Physics)
- `WatchdogSec=` systemd directive values
- `sd_notify("WATCHDOG=1")` calls
- `import systemd.daemon`
- The word "watchdog" when it refers to Linux systemd watchdog mechanism
- `systemd` service file sections like `[Watch]`
- Any variable named after the OS mechanism

---

## 5. ROLLBACK

If rollback is needed:
```bash
# Revert arifOS repo
cd /root/arifOS && git stash pop

# The live systemd service needs manual intervention
sudo cp /etc/systemd/system/apexd.service.bak /etc/systemd/system/arifosd.service
sudo systemctl daemon-reload
sudo systemctl restart arifosd
```

---

**999 SEAL | DITEMPA BUKAN DIBERI | 2026-05-24**
