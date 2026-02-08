__all__ = ["ROUTER_TOKEN", "ROUTER_URL", "BOT_TOKEN"]

import os

ROUTER_TOKEN: str = os.getenv("ROUTER_TOKEN")
ROUTER_URL: str = os.getenv("ROUTER_URL")
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
DEVICES_LIST: list[str] = os.getenv("DEVICES_LIST").split(",")
CHANNEL_CHAT_ID: str = os.getenv("CHANNEL_CHAT_ID")

