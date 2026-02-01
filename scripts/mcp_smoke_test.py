from __future__ import annotations

import argparse
import asyncio

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-test the Telegram MCP server over stdio.")
    parser.add_argument(
        "--source",
        help="Optional source to call read_messages on (must be allowlisted).",
    )
    parser.add_argument("--limit", type=int, default=5)
    return parser.parse_args()


async def _run() -> int:
    args = _parse_args()
    server_params = StdioServerParameters(command="python", args=["-m", "telegram_mcp.server"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("tools:", [tool.name for tool in tools.tools])

            sources_result = await session.call_tool("list_sources", {})
            print("list_sources:", sources_result.structuredContent)

            if args.source:
                messages_result = await session.call_tool(
                    "read_messages",
                    {"source": args.source, "limit": args.limit},
                )
                print("read_messages:", messages_result.structuredContent)

    return 0


def main() -> None:
    raise SystemExit(asyncio.run(_run()))


if __name__ == "__main__":
    main()
