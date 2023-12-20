from playwright.async_api import async_playwright, expect,Playwright
from test_cases.whatsapp_tests.test_continuous_whatsapp_responses import test_whatsapp_response,whatsapp_response
import os
import regex as re
import pandas as pd
import json


import asyncio
from playwright.async_api import async_playwright
from config.utils import (json_logger, 
                   read_excel_data)

QUESTIONAIRE = "./Mishu_question_answer_pairs.xlsx"
WHATSAPP_WEB_URL = "https://web.whatsapp.com/"
# WHATSAPP_CONTACT  = "Twilio"
TEST_CASE_NAME = "whatsapp_run"
WHATSAPP_CONTACT  = "Smith Security"



async def send_whatsapp_message(playwright: Playwright) -> None:
    logger = json_logger()
    questionaire = read_excel_data(QUESTIONAIRE)
    async with async_playwright() as p:
        # Use persistent context to reuse login state
        browser = await p.chromium.launch_persistent_context(user_data_dir='./config/user_data', headless=False)

        # Open a new page
        page = await browser.new_page()
        
        # Navigate to WhatsApp Web
        await page.goto(WHATSAPP_WEB_URL)
        # await page.get_by_role("textbox", name="Search input textbox").first.fill(WHATSAPP_CONTACT)
        # await page.get_by_role("button", name= WHATSAPP_CONTACT).click()
        # await page.locator("._13jwn").first.click(mess)
        await page.get_by_text(WHATSAPP_CONTACT).click()
        await asyncio.sleep(10)
        await whatsapp_response(page,logger)
        # await test_whatsapp_response(page,questionaire,logger)
        # await page.get_by_role("textbox", name="Type a message").fill(str(message))
        # await page.get_by_label("Send").click()
        await asyncio.sleep(10)
        await page.screenshot(path="results/videos/pictures/timeout_error_screenshot.png")


# Usage example
async def main() -> None:
    async with async_playwright() as playwright:
        await send_whatsapp_message(playwright)


asyncio.run(main())
