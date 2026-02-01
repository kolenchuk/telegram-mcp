from __future__ import annotations

from telethon import TelegramClient

from .config import Config


def build_client(config: Config) -> TelegramClient:
    return TelegramClient(
        config.session_path,
        config.api_id,
        config.api_hash,
        flood_sleep_threshold=10,
    )
