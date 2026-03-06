from __future__ import annotations

from typing import Any

from playwright.async_api import Page, Frame, FrameLocator


class BasePage:
    MAIN_FRAME_SELECTOR = "iframe#Main"
    CORE_FRAME_SELECTOR = "#coreMain"
    CORE_FRAME_NAME = "coreMain"

    def __init__(self, page: Page):
        self.page = page

    @property
    def main_frame_locator(self) -> FrameLocator:
        return self.page.frame_locator(self.MAIN_FRAME_SELECTOR)

    @property
    def core_frame_locator(self) -> FrameLocator:
        return self.main_frame_locator.frame_locator(self.CORE_FRAME_SELECTOR)

    def _get_core_frame(self) -> Frame | None:
        return self.page.frame(self.CORE_FRAME_NAME)

    @property
    def core_frame(self) -> Frame:
        frame = self._get_core_frame()
        if frame is None:
            raise RuntimeError(f"Frame '{self.CORE_FRAME_NAME}' not found")
        return frame
    
    async def eval_in_core(self, expression: str, arg: Any = None) -> Any:
        return await self.core_frame.evaluate(expression, arg)