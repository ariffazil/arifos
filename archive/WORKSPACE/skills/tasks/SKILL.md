---
name: tasks
description: "Manage tasks and projects across GitHub Projects, Linear, and Notion. Use when creating, listing, updating, or closing tasks, issues, or sprint items. Triggers: task, todo, create task, project, kanban, issue, sprint, what are my tasks, add to backlog, close task, task status, linear, github project, my tasks."
user-invocable: true
---

# Tasks & Projects Skill

Manages tasks via GitHub Projects (native), Linear (API), and Notion DB (API).

---

## Tool Selection

| Tool | Status | Best for |
|------|--------|----------|
| **GitHub Projects** | Ready (GH_TOKEN set) | Code-linked tasks, arifOS issues |
| **Notion DB** | Needs `NOTION_API_KEY` | Notes + tasks (PKM/life) |
| **Linear** | Needs `LINEAR_API_KEY` | Engineering sprints, roadmaps |

**Default routing:**
- Code/infra → GitHub Issue on `ariffazil/arifOS`
- Life/PKM → Notion DB (if `NOTION_API_KEY` set)
- Sprint/roadmap → Linear (if `LINEAR_API_KEY` set)

---

## GitHub Projects

### Create task
```bash
gh issue create -R ariffazil/arifOS \
  --title "Task title" \
  --body "Description and acceptance criteria" \
  --label "enhancement" \
  --assignee ariffazil
```

### List open tasks
```bash
gh issue list -R ariffazil/arifOS \
  --assignee ariffazil --state open --limit 20 \
  --json number,title,labels,createdAt \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    labels = ','.join([l['name'] for l in i['labels']]) or '-'
    print(f\"#{i['number']:4} [{labels:20}] {i['title']}\")
"
```

### Update / close task
```bash
gh issue edit 42 -R ariffazil/arifOS --add-label "in-progress"
gh issue close 42 -R ariffazil/arifOS --comment "Completed"
```

### View project board
```bash
gh project list --owner ariffazil
gh project item-list PROJECT_NUMBER --owner ariffazil --format json \
  | python3 -c "import sys,json; [print(i.get('title','?'),'-',i.get('status','?')) for i in json.load(sys.stdin).get('items',[])]"
```

---

## Linear

### Setup (one-time)
```bash
echo 'LINEAR_API_KEY=lin_api_YOUR_KEY_HERE' >> /root/arifOS/.env
docker compose up -d --force-recreate openclaw
```

### List assigned issues
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: ${LINEAR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { viewer { assignedIssues(first:20,filter:{state:{type:{nin:[\"completed\",\"cancelled\"]}}}) { nodes { id title priority state { name } team { name } dueDate } } } }"}' \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin)['data']['viewer']['assignedIssues']['nodes']:
    p = ['','Urgent','High','Med','Low'][i.get('priority',0)] if i.get('priority') else '-'
    print(f\"[{p:6}] [{i['state']['name']:15}] {i['title']}\")
"
```

### Create issue
```bash
TEAM_ID=$(curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: ${LINEAR_API_KEY}" -H "Content-Type: application/json" \
  -d '{"query":"query { teams { nodes { id name } } }"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['teams']['nodes'][0]['id'])")

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: ${LINEAR_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation CreateIssue(\$input:IssueCreateInput!){issueCreate(input:\$input){success issue{id title}}}\",\"variables\":{\"input\":{\"teamId\":\"${TEAM_ID}\",\"title\":\"Task title\",\"description\":\"Details\",\"priority\":3}}}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('Created:', d['data']['issueCreate']['issue']['title'])"
```

---

## Notion

```bash
TASKS_DB_ID="YOUR-NOTION-TASKS-DB-ID"

# List Todo tasks
curl -s -X POST "https://api.notion.com/v1/databases/${TASKS_DB_ID}/query" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  -d '{"filter":{"property":"Status","select":{"equals":"Todo"}},"page_size":20}' \
  | python3 -c "
import sys, json
for row in json.load(sys.stdin)['results']:
    for k,v in row['properties'].items():
        if v.get('type')=='title':
            print('  •', ''.join([t['plain_text'] for t in v['title']]))
"

# Add task
curl -s -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  -d "{\"parent\":{\"database_id\":\"${TASKS_DB_ID}\"},\"properties\":{\"Name\":{\"title\":[{\"text\":{\"content\":\"New task\"}}]},\"Status\":{\"select\":{\"name\":\"Todo\"}}}}" \
  | python3 -c "import sys,json; print('Created:', json.load(sys.stdin).get('id'))"
```
