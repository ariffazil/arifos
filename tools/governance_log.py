#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

payload = {
    'ts': datetime.now(timezone.utc).isoformat(),
    'actor': os.getenv('USER', 'unknown'),
    'event': os.getenv('EVENT', 'manual-log'),
    'note': os.getenv('NOTE', 'no-note'),
    'verdict': os.getenv('VERDICT', 'SEAL')
}
log_path = Path('/srv/arifOS/VAULT999/opencode_governance.jsonl')
log_path.parent.mkdir(parents=True, exist_ok=True)
with log_path.open('a', encoding='utf-8') as f:
    f.write(json.dumps(payload, ensure_ascii=True) + '\n')
print('logged', log_path)
