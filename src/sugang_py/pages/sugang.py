from __future__ import annotations

import asyncio
import datetime

from .base import BasePage


class SugangPage(BasePage):
    async def wait_ready(self, timeout: float = 10000.0) -> None:
        await self.core_frame_locator.locator("body").wait_for(timeout=timeout)
        await self.core_frame.wait_for_function("typeof window.fnLoad === 'function'", timeout=timeout)

    async def try_open_menu(self, timeout: float = 200.0) -> bool:
        try:
            await self.eval_in_core("fnLoad('/sugang?attribute=sugangMain', 'menu_sugang')")
            await self.core_frame.wait_for_function("typeof window.fnCallMode === 'function'", timeout=timeout)
            return True
        except:
            return False

    async def enroll(self, code: str) -> None:
        await self.eval_in_core("(code) => fnCallMode('', code, '', 'insert')", code)

    async def enroll_many(self, codes: list[str], repeat: int, interval_ms: int = 0) -> None:
        length = len(codes)
        print(datetime.datetime.now())
        for i in range(repeat):
            code = codes[i % length]
            asyncio.create_task(self.enroll(code))
            await asyncio.sleep(interval_ms / 1000.0)
        print(datetime.datetime.now())