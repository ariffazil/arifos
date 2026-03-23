FROM ghcr.io/openclaw/openclaw:latest

USER root

RUN set -eux; \
    mkdir -p /var/lib/apt/lists/partial; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates git jq; \
    rm -rf /var/lib/apt/lists/*; \
    curl -LsSf https://astral.sh/uv/install.sh | sh; \
    export PATH="/root/.local/bin:${PATH}"; \
    uv tool install --python 3.13 kimi-cli==1.18.0; \
    npm install -g opencode-ai@1.2.24 opencode-linux-x64@1.2.24; \
    for f in /root/.profile /root/.bashrc; do \
      grep -vF '. "$HOME/.local/bin/env"' "$f" > "${f}.tmp"; \
      mv "${f}.tmp" "$f"; \
    done; \
    ln -sf /root/.local/share/uv/tools/kimi-cli/bin/kimi /usr/local/bin/kimi; \
    ln -sf /usr/local/lib/node_modules/opencode-linux-x64/bin/opencode /usr/local/bin/opencode

COPY infrastructure/openclaw/openclaw-preflight.sh /usr/local/bin/openclaw-preflight
COPY infrastructure/openclaw/openclaw-entrypoint.sh /usr/local/bin/openclaw-forged-entrypoint

RUN chmod +x /usr/local/bin/openclaw-preflight /usr/local/bin/openclaw-forged-entrypoint

ENTRYPOINT ["openclaw-forged-entrypoint"]
CMD ["node","openclaw.mjs","gateway","--allow-unconfigured"]
