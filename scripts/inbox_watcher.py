import time
import os
from forge_office_document import forge_office_document

INBOX = "/watch/inbox"

def watch():
    print(f"WATCHER: Monitoring {INBOX}...")
    if not os.path.exists("/watch/processing"):
        os.makedirs("/watch/processing", exist_ok=True)
    if not os.path.exists("/watch/outbox"):
        os.makedirs("/watch/outbox", exist_ok=True)

    while True:
        try:
            for f in os.listdir(INBOX):
                if f.endswith(".md"):
                    forge_office_document(os.path.join(INBOX, f))
        except Exception as e:
            print(f"WATCHER ERROR: {e}")
        time.sleep(5)

if __name__ == "__main__":
    watch()
