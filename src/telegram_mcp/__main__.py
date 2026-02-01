from __future__ import annotations

import argparse
import asyncio
import json
import sys

from .config import Config
from .reader import read_text_messages
from .telegram_client import build_client


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read text-only messages from an allowlisted Telegram source."
    )
    parser.add_argument("--source", required=True, help="Channel/group username or ID")
    parser.add_argument("--limit", type=int, default=50)
    return parser.parse_args()


def _ensure_allowlisted(source: str, allowlist: tuple[str, ...]) -> None:
    if allowlist and source not in allowlist:
        raise ValueError(
            "Source is not allowlisted. Add it to ALLOWLIST_SOURCES."
        )

async def _run() -> int:
    args = _parse_args()
    config = Config.from_env()
    _ensure_allowlisted(args.source, config.allowlist_sources)

    client = build_client(config)
    async with client:
        await client.start()
        messages = await read_text_messages(client, args.source, args.limit)

    payload = {"source": args.source, "messages": messages}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main() -> None:
    try:
        exit_code = asyncio.run(_run())
    except Exception as exc:  # noqa: BLE001 - top-level CLI handling
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
