from __future__ import annotations

from .base import BasePage
from playwright.async_api import Locator


class LoginPage(BasePage):
    URL = "https://suganggw.gwnu.ac.kr/"

    INPUT_ID_SELECTOR = "input#id"
    INPUT_PW_SELECTOR = "input#pwd"
    BTN_LOGIN_SELECTOR = "#btn_login"

    def __init__(self, page):
        super().__init__(page)
        self._input_id: Locator | None = None
        self._input_pw: Locator | None = None
        self._btn_login: Locator | None = None

    @property
    def input_id(self) -> Locator:
        if self._input_id is None:
            self._input_id = self.main_frame_locator.locator(self.INPUT_ID_SELECTOR)
        return self._input_id

    @property
    def input_pw(self) -> Locator:
        if self._input_pw is None:
            self._input_pw = self.main_frame_locator.locator(self.INPUT_PW_SELECTOR)
        return self._input_pw

    @property
    def btn_login(self) -> Locator:
        if self._btn_login is None:
            self._btn_login = self.main_frame_locator.locator(self.BTN_LOGIN_SELECTOR)
        return self._btn_login
    
    async def open(self) -> None:
        await self.page.goto(self.URL)

    async def wait_ready(self, timeout: float = 10000.0) -> None:
        await self.input_id.wait_for(timeout=timeout)
        await self.input_pw.wait_for(timeout=timeout)
        await self.btn_login.wait_for(timeout=timeout)

    async def login(self, user_id, user_pw) -> None:
        await self.input_id.fill(user_id)
        await self.input_pw.fill(user_pw)
        await self.btn_login.click(force=True)