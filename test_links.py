import re, urllib.request, ssl
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = set()
for f in ['README.md', 'AGENTS.md']:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            urls.update(re.findall(r'https?://[^\s)\]\"\'<]+', file.read()))

print("Checking URLs...")
for url in sorted(urls):
    if 'arif-fazil' in url or 'github.com' in url:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, context=ctx, timeout=5)
            print(f'OK: {url}')
        except Exception as e:
            print(f'FAIL: {url} - {e}')
