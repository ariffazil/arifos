with open("/root/arifos/docker-compose.yml", "r") as f:
    content = f.read()

old = "test: [\"CMD-SHELL\", \"curl -sf http://geox-organ:8000/health && curl -sf http://geox-organ:8081/health && curl -sf http://vault999:8100/health && curl -sf http://redis:6379 && curl -sf http://ollama-engine-prod:11434/ && exit 0 || exit 1\"]"
new = "test: [\"CMD-SHELL\", \"python3 /tmp/sovereign_probe.py\"]"

content = content.replace(old, new)

with open("/root/arifos/docker-compose.yml", "w") as f:
    f.write(content)

print("done")
