---
name: google-workspace
description: "Access Gmail, Google Calendar, Drive, and Sheets via Google APIs. Use when reading or sending email, checking or creating calendar events, listing Drive files, or reading and writing spreadsheet data. Triggers: gmail, email, google calendar, calendar, schedule, google drive, drive, google sheets, spreadsheet, sheets, send email, check calendar, read email, upload to drive."
user-invocable: true
---

# Google Workspace Skill

Gmail, Google Calendar, Drive, and Sheets via OAuth 2.0.

Auth: OAuth 2.0 | Credentials at `~/.openclaw/gog/credentials.json` | Token at `~/.openclaw/gog/token.json`

---

## Setup (One-Time OAuth Flow)

```bash
cd /opt/arifos/data/openclaw/gog
pip3 install --quiet google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client 2>/dev/null

python3 << 'PYEOF'
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets',
]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
with open('token.json', 'w') as f:
    f.write(creds.to_json())
print("Token saved to token.json")
PYEOF
```

Token auto-refreshes via `google-auth` — no re-auth needed unless revoked.

---

## Gmail

### Read unread emails
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('gmail', 'v1', credentials=creds)
results = service.users().messages().list(userId='me', q='is:unread', maxResults=10).execute()
for msg in results.get('messages', [])[:5]:
    m = service.users().messages().get(userId='me', id=msg['id'], format='metadata',
        metadataHeaders=['Subject','From','Date']).execute()
    h = {x['name']: x['value'] for x in m['payload']['headers']}
    print(h.get('From'), '|', h.get('Subject'), '|', h.get('Date'))
```

### Send email
```python
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('gmail', 'v1', credentials=creds)
msg = MIMEText("Email body here")
msg['to'] = 'recipient@example.com'
msg['subject'] = 'Subject here'
result = service.users().messages().send(
    userId='me', body={'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
).execute()
print(f"Sent: {result['id']}")
```

> F11: Sending email is high-visibility — state intent clearly before executing.

---

## Google Calendar

### View upcoming events
```python
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('calendar', 'v3', credentials=creds)
events = service.events().list(
    calendarId='primary', timeMin=datetime.now(timezone.utc).isoformat(),
    maxResults=10, singleEvents=True, orderBy='startTime'
).execute().get('items', [])
for e in events:
    start = e['start'].get('dateTime', e['start'].get('date'))
    print(f"  {start} — {e.get('summary','(no title)')}")
```

### Create event
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('calendar', 'v3', credentials=creds)
event = {
    'summary': 'Event Title',
    'start': {'dateTime': '2026-03-08T10:00:00+08:00', 'timeZone': 'Asia/Kuala_Lumpur'},
    'end':   {'dateTime': '2026-03-08T11:00:00+08:00', 'timeZone': 'Asia/Kuala_Lumpur'},
}
result = service.events().insert(calendarId='primary', body=event).execute()
print(f"Created: {result.get('htmlLink')}")
```

> Timezone: Always use `Asia/Kuala_Lumpur` for Malaysian events.

---

## Google Drive

### List recent files
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('drive', 'v3', credentials=creds)
files = service.files().list(
    pageSize=15, fields='files(id,name,mimeType,modifiedTime)', orderBy='modifiedTime desc'
).execute().get('files', [])
for f in files:
    print(f"{f['modifiedTime'][:10]} | {f['mimeType'].split('.')[-1]:20} | {f['name']}")
```

---

## Google Sheets

### Read range
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SHEET_ID = 'YOUR_SPREADSHEET_ID'
creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('sheets', 'v4', credentials=creds)
rows = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range='Sheet1!A1:E20'
).execute().get('values', [])
for row in rows:
    print('\t'.join(row))
```

### Append row
```python
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SHEET_ID = 'YOUR_SPREADSHEET_ID'
creds = Credentials.from_authorized_user_file('/home/node/.openclaw/gog/token.json')
service = build('sheets', 'v4', credentials=creds)
service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID, range='Sheet1',
    valueInputOption='USER_ENTERED',
    body={'values': [[datetime.now().strftime('%Y-%m-%d %H:%M'), 'New row', 'data']]}
).execute()
print("Row appended")
```

---

## Notes

- Token lives at `~/.openclaw/gog/token.json` — gitignored, never commit
- Scopes: gmail read+send, calendar read+write, drive read, sheets read+write
