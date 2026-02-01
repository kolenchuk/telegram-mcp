from __future__ import annotations

import argparse
import asyncio
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from .config import Config
from .reader import read_text_messages
from .telegram_client import build_client


SERVER_NAME = "telegram-mcp"
SERVER_VERSION = "0.1.0"


def _ensure_allowlisted(source: str, allowlist: tuple[str, ...]) -> None:
    if allowlist and source not in allowlist:
        raise ValueError("Source is not allowlisted. Add it to ALLOWLIST_SOURCES.")


def _error_result(message: str) -> types.CallToolResult:
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=message)],
        isError=True,
    )


server = Server(SERVER_NAME)


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_sources",
            description="List allowlisted Telegram sources.",
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
            outputSchema={
                "type": "object",
                "properties": {"sources": {"type": "array", "items": {"type": "string"}}},
                "required": ["sources"],
            },
        ),
        types.Tool(
            name="read_messages",
            description="Read text-only messages from a Telegram source.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 500},
                },
                "required": ["source"],
                "additionalProperties": False,
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "ts": {"type": "string"},
                                "text": {"type": "string"},
                            },
                            "required": ["id", "ts", "text"],
                        },
                    },
                },
                "required": ["source", "messages"],
            },
        ),
        types.Tool(
            name="get_checkpoint",
            description="Get the last processed message ID for a source (not yet persisted).",
            inputSchema={
                "type": "object",
                "properties": {"source": {"type": "string"}},
                "required": ["source"],
                "additionalProperties": False,
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "last_message_id": {"type": ["integer", "null"]},
                },
                "required": ["source", "last_message_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any] | types.CallToolResult:
    if name == "list_sources":
        config = Config.from_env()
        return {"sources": list(config.allowlist_sources)}

    if name == "read_messages":
        source = str(arguments.get("source", "")).strip()
        if not source:
            return _error_result("Missing required argument: source")
        limit = arguments.get("limit", 50)
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            return _error_result("limit must be an integer")

        config = Config.from_env()
        try:
            _ensure_allowlisted(source, config.allowlist_sources)
        except ValueError as exc:
            return _error_result(str(exc))

        client = build_client(config)
        async with client:
            await client.start()
            messages = await read_text_messages(client, source, limit)
        return {"source": source, "messages": messages}

    if name == "get_checkpoint":
        source = str(arguments.get("source", "")).strip()
        if not source:
            return _error_result("Missing required argument: source")
        return {"source": source, "last_message_id": None}

    raise ValueError(f"Unknown tool: {name}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Telegram MCP server (stdio).")
    parser.add_argument("--stdio", action="store_true", help="Use stdio transport (default)")
    return parser.parse_args()


async def run() -> None:
    _parse_args()
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version=SERVER_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
