import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    with open(ENV_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GITHUB_URL = "https://github.com/dc-voltage"
JFC_GITHUB_URL = "https://github.com/JFC-Group"
TELEGRAM_GROUP_URL = "https://t.me/JIo_Airtel_Unlock"
COMMUNITY_CHAT_ID = int(os.getenv("COMMUNITY_CHAT_ID", "-1003098658474"))
FILES_DIR = BASE_DIR / "files"
ADMIN_USER_IDS = [int(x.strip()) for x in os.getenv("ADMIN_USER_IDS", "5529014682").split(",") if x.strip()]
if 5529014682 not in ADMIN_USER_IDS:
    ADMIN_USER_IDS.append(5529014682)
