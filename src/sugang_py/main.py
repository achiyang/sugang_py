from __future__ import annotations

import asyncio

from playwright.async_api import async_playwright
from datetime import timedelta

from config import load_settings
from pages.login import LoginPage
from pages.sugang import SugangPage
from utils.time import wait_until


async def run() -> None:
    s = load_settings()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=s.headless)
        context = await browser.new_context()
        page = await context.new_page()

        login = LoginPage(page)
        sugang = SugangPage(page)

        try:
            # 1. 로그인
            await login.open()
            await login.wait_ready()
            await login.login(s.user_id, s.user_pw)

            # 2. 프레임 및 메뉴 준비
            await sugang.wait_ready()
            while True:
                if await sugang.try_open_menu():
                    break

            # 3. 시간 대기
            if s.target_at is not None:
                await wait_until(s.target_at - timedelta(milliseconds=300))

            # 4. 수강신청 패킷 전송
            await sugang.enroll_many(s.subject_codes, s.repeat, s.interval_ms)

        except Exception as e:
            print(f"[ERROR] {e}")

        # 브라우저가 닫히지 않도록 대기
        await asyncio.to_thread(input)

if __name__ == "__main__":
    asyncio.run(run())