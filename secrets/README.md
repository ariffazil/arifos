# arifOS Secrets Directory

**WARNING:** This directory contains sensitive cryptographic material.
**DO NOT** commit these files to Git.

## Files

- `governance.secret` - The ARIFOS_GOVERNANCE_SECRET for signing auth_context\n## Usage

Set in your environment:
```bash
export ARIFOS_GOVERNANCE_SECRET_FILE=/opt/arifos/secrets/governance.secret
```

Or use the .env.production file which references this path.

## Rotation

To rotate the secret:
1. Generate new secret: `python -c "import secrets; print(secrets.token_hex(32))"`
2. Write to governance.secret.new
3. Set ARIFOS_GOVERNANCE_SECRET_PREVIOUS_FILE to old secret path
4. Update governance.secret with new content
5. Restart service
6. Remove old secret after verifying new signatures work
