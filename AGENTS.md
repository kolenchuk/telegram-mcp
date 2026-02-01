# Repository Guidelines

## Project Structure & Module Organization
This repository currently contains:
- `.planning/`: planning brief artifacts and project history (see `history.md`).
- `src/`: implementation code.
- `telegram-analiser-mcp-prd.md`: PRD describing the Telegram MCP Reader scope, goals, and constraints.

If you add code, keep a clear top-level layout (example: `src/` for implementation, `tests/` for tests, `scripts/` for tooling, `configs/` for runtime configuration). Document any new directories here.

## Build, Test, and Development Commands
No build, test, or run scripts are defined yet. When adding them, include exact commands and what they do. Example format:
- `make build` — build the MCP server binary
- `make test` — run the full test suite
- `python -m app` — start the local server
 - `PYTHONPATH=src python -m telegram_mcp --source <source> --limit 50` — read text messages from an allowlisted source

## Documentation & References
Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.

## Skills
- `telethon-client-ops` — Canonical patterns for Telethon auth, session handling, peer resolution, and rate-limit retries; includes a session validation script.
- `mcp-python-tooling` — MCP Python 3.12 server setup, tool registration patterns, error schema, and response payload conventions.
- `telegram-mcp-domain-expertise` — Domain expertise map for Telegram MCP Reader (Telethon + MCP protocol conventions).
- `mcp-tool-design` — MCP tool design guidance for schemas, structured outputs, and error conventions.

## Coding Style & Naming Conventions
No language-specific standards are defined yet. Follow these defaults until code exists:
- Match the existing file style (Markdown headings and concise paragraphs).
- Prefer kebab-case for new Markdown filenames (example: `agent-setup.md`).
- Keep line lengths reasonable for readability and avoid excessive wrapping.

If you introduce a formatter or linter, add its command and expectations here (example: `ruff format` or `prettier --check`).

## Testing Guidelines
There is no test framework configured yet. When tests are added:
- Use a `tests/` directory and mirror the source layout.
- Name tests with clear intent (example: `test_checkpoint_store.py`).
- Document the command to run a single test and the full suite.

## Commit & Pull Request Guidelines
No Git history is available in this repository, so no established convention exists. Use Conventional Commits as a default:
- `feat: add checkpoint store`
- `fix: handle duplicate message IDs`

Pull requests should include:
- A short summary of changes and rationale.
- Any linked issues or tickets.
- Test evidence (commands run and results) or a note explaining why tests are not applicable.

## Security & Configuration Tips
This project is expected to use Telegram user credentials and session files. Do not commit secrets. Keep configuration in local files (example: `configs/local.env`) and add any sensitive paths to `.gitignore` when the repo is initialized.
