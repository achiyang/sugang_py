from __future__ import annotations

from playwright.async_api import Locator

from .base import BasePage


class LoginPage(BasePage):
    URL = "https://suganggw.gwnu.ac.kr/"

    INPUT_ID_SELECTOR = "input#id"
    INPUT_PW_SELECTOR = "input#pwd"
    BTN_LOGIN_SELECTOR = "#btn_login"

    @property
    def input_id(self) -> Locator:
        return self.main_frame_locator.locator(self.INPUT_ID_SELECTOR)

    @property
    def input_pw(self) -> Locator:
        return self.main_frame_locator.locator(self.INPUT_PW_SELECTOR)

    @property
    def btn_login(self) -> Locator:
        return self.main_frame_locator.locator(self.BTN_LOGIN_SELECTOR)
    
    async def open(self) -> None:
        await self.page.goto(self.URL)

    async def wait_ready(self, timeout: float = 10_000) -> None:
        await self.input_id.wait_for(timeout=timeout)
        await self.input_pw.wait_for(timeout=timeout)
        await self.btn_login.wait_for(timeout=timeout)

    async def login(self, user_id: str, user_pw: str) -> None:
        await self.input_id.fill(user_id)
        await self.input_pw.fill(user_pw)
        await self.btn_login.click()