from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os

from dotenv import load_dotenv


def _parse_bool(v: str | None, default: bool) -> bool:
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "t", "yes", "y", "on")


def _parse_int(v: str | None, default: int) -> int:
    if v is None or not v.strip():
        return default
    return int(v)


def _parse_codes(v: str | None) -> list[str]:
    if not v:
        return []
    return [x.strip() for x in v.split(",") if x.strip()]


def _parse_dt(v: str | None) -> datetime | None:
    if not v:
        return None
    return datetime.fromisoformat(v) if v else None


@dataclass(frozen=True)
class Settings:
    user_id: str
    user_pw: str
    subject_codes: list[str]
    target_at: datetime | None

    headless: bool = False
    repeat: int = 50
    interval_ms: int = 10
    advance_ms: int = 0


def load_settings() -> Settings:
    load_dotenv()

    user_id = os.getenv("SUGANG_USER_ID", "").strip()
    user_pw = os.getenv("SUGANG_USER_PW", "").strip()
    subject_codes = _parse_codes(os.getenv("SUGANG_SUBJECT_CODES"))
    target_at = _parse_dt(os.getenv("SUGANG_TARGET_AT"))

    headless = _parse_bool(os.getenv("SUGANG_HEADLESS"), False)
    repeat = _parse_int(os.getenv("SUGANG_REPEAT"), 50)
    interval_ms = _parse_int(os.getenv("SUGANG_INTERVAL_MS"), 10)
    advance_ms = _parse_int(os.getenv("SUGANG_ADVANCE_MS"), 0)

    if not user_id:
        raise ValueError("SUGANG_USER_ID is empty")
    if not user_pw:
        raise ValueError("SUGANG_USER_PW is empty")
    if not subject_codes:
        raise ValueError("SUGANG_SUBJECT_CODES is empty")
    if repeat <= 0:
        raise ValueError("SUGANG_REPEAT must be > 0")

    return Settings(
        user_id=user_id,
        user_pw=user_pw,
        subject_codes=subject_codes,
        target_at=target_at,
        headless=headless,
        repeat=repeat,
        interval_ms=interval_ms,
        advance_ms=advance_ms
    )