from __future__ import annotations

from datetime import timezone
from typing import Any

from telethon import TelegramClient


async def read_text_messages(
    client: TelegramClient,
    source: str,
    limit: int = 50,
) -> list[dict[str, Any]]:
    entity = await client.get_input_entity(source)
    messages: list[dict[str, Any]] = []

    async for message in client.iter_messages(entity, limit=limit):
        if not message.message:
            continue
        timestamp = message.date
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        messages.append(
            {
                "id": message.id,
                "ts": timestamp.isoformat(),
                "text": message.message,
            }
        )

    # iter_messages returns newest-first; reverse for chronological order.
    messages.reverse()
    return messages
