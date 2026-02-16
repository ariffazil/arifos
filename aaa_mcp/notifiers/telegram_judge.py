# aaa_mcp/notifiers/telegram_judge.py — F11 Command Authority
"""
888 Judge Notification System
Human-in-the-loop untuk constitutional escalation.
"""

import os
from typing import Dict


class TelegramJudge:
    """F11 Command Authority: Human override via Telegram."""

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.bot_token and self.chat_id)

    async def notify_888_hold(self, verdict_context: Dict) -> Dict:
        """
        Notify 888 Judge when constitutional hold triggered.

        Args:
            verdict_context: {
                "session_id": str,
                "floor_violated": str,
                "reason": str,
                "verdict": str,
                "risk_level": str
            }

        Returns:
            {"sent": bool, "message_id": str, "error": str}
        """
        if not self.enabled:
            return {
                "sent": False,
                "error": "Telegram not configured (TELEGRAM_BOT_TOKEN or CHAT_ID missing)",
                "mode": "DEGRADED_F11",
            }

        message = f"""🛡️ <b>888 HOLD TRIGGERED</b>

<b>Floor:</b> {verdict_context.get('floor_violated', 'UNKNOWN')}
<b>Reason:</b> {verdict_context.get('reason', 'Constitutional violation detected')}
<b>Session:</b> <code>{verdict_context.get('session_id', 'N/A')}</code>
<b>Verdict:</b> {verdict_context.get('verdict', 'VOID')}
<b>Risk:</b> {verdict_context.get('risk_level', 'unknown')}

<i>Reply /APPROVE atau /VOID</i>

<code>DITEMPA BUKAN DIBERI</code> 🔥
"""

        try:
            import httpx

            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": "✅ APPROVE",
                                "callback_data": f"APPROVE:{verdict_context.get('session_id')}",
                            },
                            {
                                "text": "❌ VOID",
                                "callback_data": f"VOID:{verdict_context.get('session_id')}",
                            },
                        ]
                    ]
                },
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                data = response.json()

                if data.get("ok"):
                    return {
                        "sent": True,
                        "message_id": data["result"]["message_id"],
                        "chat_id": self.chat_id,
                        "mode": "SOVEREIGN_F11",
                    }
                else:
                    return {
                        "sent": False,
                        "error": data.get("description", "Unknown error"),
                        "mode": "DEGRADED_F11",
                    }

        except Exception as e:
            return {"sent": False, "error": str(e), "mode": "DEGRADED_F11"}

    async def send_status(self, message: str) -> bool:
        """Send status update ke 888 Judge."""
        if not self.enabled:
            return False

        try:
            import httpx

            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"}

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                return response.json().get("ok", False)

        except Exception:
            return False


# Global instance
judge = TelegramJudge()
