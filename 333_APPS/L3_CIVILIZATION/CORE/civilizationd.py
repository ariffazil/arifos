"""
L6_CIVILIZATION: Clockmaker Daemon
Canon: C:/Users/User/arifOS/333_APPS/L6_CIVILIZATION/civilizationd.py

The heartbeat of the arifOS civilization. A long-running process that 
wakes up agents asynchronously based on time or external criteria.

Rules:
- It NEVER touches disk or Docker directly.
- It ONLY publishes events to the Town Square (Redis), triggering MCP tools.
"""

import time
import logging
import schedule
from .town_square import CivilizationBus, TOPIC_JOB_AUDIT, TOPIC_JOB_NEWS

logging.basicConfig(level=logging.INFO, format="[STAGE 000] Clockmaker | %(message)s")
logger = logging.getLogger("civilizationd")

class ClockmakerDaemon:
    
    def __init__(self, bus: CivilizationBus):
        self.bus = bus
        self._setup_schedule()
        
    def _setup_schedule(self):
        """Maps tasks to times using the schedule library."""
        # 03:00 AM - Audit Ledger (Soul/APEX pipe)
        schedule.every().day.at("03:00").do(self.trigger_audit)
        
        # Hourly - Gather News (Mind agent pipe)
        schedule.every(1).hours.do(self.trigger_news_refresh)
        
        logger.info("Clockmaker schedule initialized. Waiting for ticks...")

    def trigger_audit(self):
        logger.info("Tick: 03:00. Triggering Daily Audit.")
        self.bus.publish_event(TOPIC_JOB_AUDIT, {
            "source": "clockmaker",
            "action": "trigger_apex_audit",
            "target": "soul_agent"
        })

    def trigger_news_refresh(self):
        logger.info("Tick: Hourly. Triggering News Refresh.")
        self.bus.publish_event(TOPIC_JOB_NEWS, {
            "source": "clockmaker",
            "action": "scrape_curated_feeds",
            "target": "mind_agent"
        })

    def run_forever(self):
        """Main event loop."""
        logger.info("Civilization Daemon started. The city is alive.")
        target_ticks = 0
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
                target_ticks += 1
                if target_ticks % 3600 == 0:
                    logger.info("Clockmaker heartbeat OK.")
        except KeyboardInterrupt:
            logger.info("Civilization Daemon shutting down gracefully.")

if __name__ == "__main__":
    # Test execution
    bus = CivilizationBus()
    daemon = ClockmakerDaemon(bus=bus)
    # Testing a singular trigger
    daemon.trigger_audit()
