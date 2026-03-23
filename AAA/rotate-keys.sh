#!/bin/bash
# ============================================================
# ARIFOS API KEY ROTATION SCRIPT
# Run this to identify which keys need rotation
# ============================================================

echo "=========================================="
echo "API KEY ROTATION AUDIT"
echo "=========================================="
echo ""
echo "⚠️  WARNING: The following API keys have been EXPOSED"
echo "   in chat logs and should be ROTATED immediately:"
echo ""

cat << 'KEYS'
🔴 CRITICAL - Rotate Immediately:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. OPENAI_API_KEY
   Current: sk-proj-28kKv...hVoA
   Status: EXPOSED in chat
   Action: Generate new key at https://platform.openai.com/api-keys

2. DEEPSEEK_API_KEY
   Current: sk-c6c737...6261a0
   Status: EXPOSED in chat
   Action: Generate new key at https://platform.deepseek.com/api_keys

3. VENICE_API_KEY
   Current: VENICE-ADMIN-KEY-P8ceoDt6utls...
   Status: EXPOSED in chat
   Action: Generate new key at https://venice.ai/settings/api

4. OPENROUTER_API_KEY
   Current: sk-or-v1-2531c855...
   Status: EXPOSED in chat
   Action: Generate new key at https://openrouter.ai/keys

5. MOONSHOT_API_KEY
   Current: sk-MNuBJMLnVIrRxl7...
   Status: EXPOSED in chat
   Action: Generate new key at https://platform.moonshot.cn/

6. KIMI_API_KEY
   Current: sk-kimi-wkZioFlp6N2...
   Status: EXPOSED in chat
   Action: Generate new key at Moonshot platform

7. MINIMAX_API_KEY
   Current: sk-api-GaY9uchvyjQ...
   Status: EXPOSED in chat
   Action: Generate new key at https://www.minimaxi.com/

8. MISTRAL_API_KEY
   Current: eaYngJhnKfgtBCaFRv...
   Status: EXPOSED in chat
   Action: Generate new key at https://console.mistral.ai/

9. BRAVE_API_KEY
   Current: BSAHQnxf-jTMFfGYe3MK...
   Status: EXPOSED in chat
   Action: Generate new key at https://api.search.brave.com/app/keys

10. PERPLEXITY_API_KEY
    Current: pplx-uAAs7RWYwvRhltTPU...
    Status: EXPOSED in chat
    Action: Generate new key at https://www.perplexity.ai/settings/api

11. FIRECRAWL_API_KEY
    Current: fc-733871f346c14a82947a6...
    Status: EXPOSED in chat
    Action: Generate new key at https://www.firecrawl.dev/app/api-keys

12. CONTEXT7_API_KEY
    Current: ctx7sk-1dd34375-5d0c...
    Status: EXPOSED in chat
    Action: Generate new key at Context7 dashboard

13. GREPTILE_API_KEY
    Current: 4UGltDc74eq/4DYOugN5xFz...
    Status: EXPOSED in chat
    Action: Generate new key at https://app.greptile.com/

14. GITHUB_TOKEN
    Current: github_pat_11BSI7YTQ0TrdLQc...
    Status: EXPOSED in chat
    Action: Generate new token at https://github.com/settings/tokens

15. TELEGRAM_BOT_TOKEN
    Current: 8149595687:AAFzuUinflxbus...
    Status: EXPOSED in chat
    Action: Revoke and regenerate via @BotFather

16. BROWSERLESS_TOKEN
    Current: sfLnosV5jRzzgjeAspPrbf226...
    Status: EXPOSED in chat
    Action: Generate new token in Browserless dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 SECURITY TOKENS:
- ROOT_PASSWORD: g7e9Sttr13v4P108TFaOgqtA4Iioa5un
- OPENCLAW_GATEWAY_TOKEN: 8a6c99b0d042f56233af05b86cf5eae06b0d31a77dddc359e56375f7fe5e1a15
- N8N_BASIC_AUTH_PASSWORD: g7e9Sttr13v4P108TFaOgqtA4Iioa5un

All of the above should be changed!
KEYS

echo ""
echo "=========================================="
echo "NEXT STEPS:"
echo "=========================================="
echo ""
echo "1. Generate new keys at each provider website"
echo "2. Update /root/agi-stack/.env with new keys"
echo "3. Run: docker compose -f docker-compose.lab.yml restart"
echo "4. Delete old/revoked keys from provider dashboards"
echo "5. Clear shell history: history -c && history -w"
echo ""
echo "⚠️  Remember: All keys exposed in this session are compromised!"
echo ""
