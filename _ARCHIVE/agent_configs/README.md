## Agent Config Relocation Notice

On 2026-02-22, root-level agent config directories were moved to reduce root entropy:

- `.agents` -> `_ARCHIVE/agent_configs/.agents`
- `.antigravity` -> `_ARCHIVE/agent_configs/.antigravity`
- `.kimi` -> `_ARCHIVE/agent_configs/.kimi`
- `.openmcp` -> `_ARCHIVE/agent_configs/.openmcp`
- `.clawhub` -> `_ARCHIVE/agent_configs/.clawhub`

If any local scripts/tools still reference old root paths, update them to use the archived paths above.
