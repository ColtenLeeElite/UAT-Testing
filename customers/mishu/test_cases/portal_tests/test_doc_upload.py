import asyncio
import logging
from playwright.async_api import Playwright, async_playwright, expect
from playwright.async_api import Page
from playwright.async_api import TimeoutError, Error
import logging
import json
import pytest
import os
import regex as re
import pandas as pd
# from config.utils import (json_logger,
#                           read_excel_data)
# from test_cases.test_pin_agent import test_pin_agent
WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "maya-agent-test.pdf"
PROMPT_FILE = "prompt-template.xlsx"
BASE_URL = "http://localhost:3000"
TEST_CASE_NAME = "test_doc_upload"
AGENT_NAME = ['Ava']
DOCUMENT_URL = ['https://doordash.engineering/category/backend/']


async def test_upload_file(page, agent):
    try:
        await page.locator('[role="Agent"]').filter(has_text=agent).click()
        await page.locator('[role="MenuList"]').filter(has_text=agent).click()
        await page.locator('[role="menuitem"]').filter(has_text='Edit').click()
        await page.get_by_text("Documents", exact=True).click()
        # await page.get_by_text("Drop files here or click to select files").set_input_files(FILE_TO_UPLOAD)
        await page.locator('[role="file"]').set_input_files(FILE_TO_UPLOAD)
        await page.get_by_role("button", name="Upload").click()

        # Log success
        # logger.info(json.dumps(
        #     {"result": f"passed{TEST_CASE_NAME}", "detail": "File uploaded successfully"}))
    except Exception as e:
        # logger.error(json.dumps(
        #     {"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))
        print('')


async def run(playwright: Playwright) -> None:
    # logger = json_logger()
    # prompt_data = read_excel_data(PROMPT_FILE)
    # prompt_data = await read_prompt_data(PROMPT_FILE)
    browser = await playwright.chromium.launch(slow_mo=1000, channel="chrome", headless=False)
    context = await browser.new_context(storage_state='./auth.json')
    # record_video_dir="results/videos/",
    # record_video_size={"width": 640, "height": 480}

    page = await context.new_page()
    await browser.start_tracing(path="results/tracing/trace.json")
    await context.tracing.start(screenshots=True, snapshots=True)
    await page.goto(BASE_URL)
    await page.get_by_text("Login with Google").click()
    await page.locator("button").filter(has_text="Agents").click()
    for agent in AGENT_NAME:
        await test_upload_file(page, agent,)

    # ---------------------
    browser.stop_tracing()
    await context.tracing.stop(path="results/tracing/trace1.zip")
    await context.storage_state(path="auth.json")
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
