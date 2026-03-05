from __future__ import annotations

import asyncio
from datetime import datetime


def _now_local() -> datetime:
    return datetime.now().astimezone()

async def wait_until(target_at: datetime) -> None:
    if target_at.tzinfo is None:
        target_at = target_at.replace(tzinfo=_now_local().tzinfo)

    while True:
        now = _now_local()
        remaining = (target_at - now).total_seconds()
        if remaining <= 0:
            return
        
        sleep_s = max(remaining / 2, 0.05)
        await asyncio.sleep(sleep_s)