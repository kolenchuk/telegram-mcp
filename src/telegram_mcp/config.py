from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    api_id: int
    api_hash: str
    session_path: str
    allowlist_sources: tuple[str, ...]

    @classmethod
    def from_env(cls) -> "Config":
        _load_env_file(".env.local")
        missing: list[str] = []
        api_id_raw = os.getenv("TELEGRAM_API_ID")
        if not api_id_raw:
            missing.append("TELEGRAM_API_ID")
        api_hash = os.getenv("TELEGRAM_API_HASH")
        if not api_hash:
            missing.append("TELEGRAM_API_HASH")

        if missing:
            raise ValueError("Missing required env vars: " + ", ".join(missing))

        session_path = os.getenv("TELEGRAM_SESSION_PATH", "telegram.session")
        allowlist_sources = _split_csv(os.getenv("ALLOWLIST_SOURCES", ""))

        return cls(
            api_id=int(api_id_raw),
            api_hash=api_hash,
            session_path=session_path,
            allowlist_sources=allowlist_sources,
        )


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(",") if part.strip())


def _load_env_file(path: str) -> None:
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[len("export ") :]
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    continue
                if (
                    (value.startswith('"') and value.endswith('"'))
                    or (value.startswith("'") and value.endswith("'"))
                ):
                    value = value[1:-1]
                os.environ.setdefault(key, value)
    except OSError as exc:
        raise ValueError(f"Failed to read env file {path}: {exc}") from exc
