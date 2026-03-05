from __future__ import annotations

from typing import Any

from playwright.async_api import Page, Frame, FrameLocator


class BasePage:
    MAIN_FRAME_SELECTOR = "iframe#Main"
    CORE_FRAME_SELECTOR = "#coreMain"
    CORE_FRAME_NAME = "coreMain"

    def __init__(self, page: Page):
        self.page = page
        self._main_frame_locator: FrameLocator | None = None
        self._core_frame_locator: FrameLocator | None = None
        self._core_frame: Frame | None = None

    @property
    def main_frame_locator(self) -> FrameLocator:
        if self._main_frame_locator is None:
            self._main_frame_locator = self.page.frame_locator(self.MAIN_FRAME_SELECTOR)
        return self._main_frame_locator

    @property
    def core_frame_locator(self) -> FrameLocator:
        if self._core_frame_locator is None:
            self._core_frame_locator = self.main_frame_locator.frame_locator(self.CORE_FRAME_SELECTOR)
        return self._core_frame_locator

    @property
    def core_frame(self) -> Frame | None:
        if self._core_frame is None or self._core_frame.is_detached():
            self._core_frame = self.page.frame(self.CORE_FRAME_NAME)
        return self._core_frame
    
    async def eval_in_core(self, expression: str, arg: Any = None) -> Any:
        return await self.core_frame.evaluate(expression, arg)