---
name: browser
description: "Automate a real Chromium browser to screenshot, scrape, fill forms, or save pages as PDF. Use when navigating to URLs, capturing screenshots, extracting page content, automating web forms, or monitoring web services. Triggers: open browser, screenshot, take a screenshot, scrape page, get page content, fill form, navigate to, render page, save as pdf, web automation, click on, browser automation, full page, visit."
user-invocable: true
---

# Browser Skill

Real browser automation via Browserless Chromium 145 at `http://headless_browser:3000`.
No token required — internal Docker network (`arifos_trinity`).

---

## Method 1 — OpenClaw Native Tool

Use for interactive navigation, clicking, and form-filling.

```
browser: navigate to https://example.com
browser: click on "Submit" button
browser: fill input[name=email] with "arif@example.com"
browser: get page text
browser: take screenshot
```

---

## Method 2 — Browserless REST API

Use for precise control, bulk operations, or scripted workflows.

### Screenshot
```bash
curl -s -X POST http://headless_browser:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url":"https://YOURURL.com","options":{"fullPage":true,"type":"png"}}' \
  -o ~/.openclaw/workspace/logs/screenshot_$(date +%s).png
```

### Get page content
```bash
curl -s -X POST http://headless_browser:3000/content \
  -H "Content-Type: application/json" \
  -d '{"url":"https://YOURURL.com","rejectResourceTypes":["image","font","stylesheet"],"waitForSelector":"body"}' \
  | head -200
```

### Scrape elements
```bash
curl -s -X POST http://headless_browser:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://YOURURL.com","elements":[{"selector":"h1"},{"selector":".price"},{"selector":"article p"}]}' \
  | python3 -c "
import sys, json
for block in json.load(sys.stdin)['data']:
    print(f\"=== {block['selector']} ===\")
    for r in block['results'][:5]: print(r['text'])
"
```

### Save as PDF
```bash
curl -s -X POST http://headless_browser:3000/pdf \
  -H "Content-Type: application/json" \
  -d '{"url":"https://YOURURL.com","options":{"printBackground":true,"format":"A4","margin":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}}}' \
  -o ~/.openclaw/workspace/logs/page_$(date +%s).pdf
```

### Execute custom JavaScript
```bash
curl -s -X POST http://headless_browser:3000/function \
  -H "Content-Type: application/json" \
  -d '{
    "code": "module.exports = async ({ page }) => {
      await page.goto(\"https://YOURURL.com\");
      const title = await page.title();
      const links = await page.$$eval(\"a\", els => els.map(e => ({text: e.textContent.trim(), href: e.href})).filter(l => l.text).slice(0,20));
      return { title, links };
    }"
  }' | python3 -m json.tool
```

---

## Common Workflows

### Check if site is up
```bash
curl -s -X POST http://headless_browser:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://TARGET.com","elements":[{"selector":"title"},{"selector":"h1"}]}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); [print(b['selector'],':',b['results'][0]['text'] if b['results'] else 'empty') for b in d['data']]"
```

### Monitor VPS domains
```bash
for DOMAIN in arifosmcp.arif-fazil.com claw.arifosmcp.arif-fazil.com flow.arifosmcp.arif-fazil.com; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://${DOMAIN}" --max-time 5)
  echo "${DOMAIN}: HTTP ${STATUS}"
done
```

### Screenshot Grafana dashboard
```bash
curl -s -X POST http://headless_browser:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url":"http://arifos_grafana:3000","options":{"fullPage":true}}' \
  -o ~/.openclaw/workspace/logs/grafana_$(date +%Y%m%d).png
```

---

## Notes

- Output files: save to `~/.openclaw/workspace/logs/` for git tracking
- Large scrapes: add `"rejectResourceTypes":["image","font","media"]` to speed up
- Login automation (F11): state intent and get confirmation before handling credentials
