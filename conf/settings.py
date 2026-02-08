__all__ = [
    "BASE_DIR", "TEMPLATE_DIR", "STORAGE_FILE",
    "ROUTER_TOKEN", "ROUTER_URL", "ROUTER_USERNAME", "ROUTER_PASSWORD",
    "BOT_TOKEN"
]

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
TEMPLATE_DIR = BASE_DIR / "templates"
STORAGE_FILE = BASE_DIR / "data" / "storage.json"

load_dotenv(ENV_FILE)

ROUTER_TOKEN: str = os.getenv("ROUTER_TOKEN")
ROUTER_URL: str = os.getenv("ROUTER_URL")
ROUTER_USERNAME: str = os.getenv("ROUTER_USERNAME")
ROUTER_PASSWORD: str = os.getenv("ROUTER_PASSWORD")

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
DEVICES_LIST: list[str] = os.getenv("DEVICES_LIST").split(",")
CHANNEL_CHAT_ID: str = os.getenv("CHANNEL_CHAT_ID")
