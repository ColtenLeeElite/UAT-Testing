
import asyncio
import logging
from playwright.async_api import Playwright, async_playwright, expect
from playwright.async_api import Page
from playwright.async_api import TimeoutError,Error
import logging
import json
import pytest
import os
import regex as re
import pandas as pd
# import config
from config.utils import (json_logger, 
                   read_excel_data)
from test_cases.portal_tests.test_continuous_response import test_chat_response
from test_cases.portal_tests.test_create_agent import pic_upload, fill_form

from test_cases.portal_tests.test_doc_upload import test_upload_file
from test_cases.portal_tests.test_pin_agent import test_pin_agent
from test_cases.portal_tests.test_add_url import test_add_url
WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "./maya-agent-test.pdf"
PROMPT_FILE = "prompt-template.xlsx"
BASE_URL= "https://azara-ai-dev-server.vercel.app/agents"
TEST_CASE_NAME = "test_doc_upload"
AGENT_PIC = "Maya-agent.jpg"

QUESTIONAIRE = "Mishu_question_answer_pairs.xlsx"
AGENT_NAME = ['Ava']
# CLIENT_FILE_PATH = "./Mishu_files"
DOCUMENT_URL = ['mishu.my/blog/company-incorporation-and-formation/labuan-protected-cell-company/']
async def run(playwright: Playwright) -> None:
    logger = json_logger()
    prompt_data = read_excel_data(PROMPT_FILE)
    questionaire = read_excel_data(QUESTIONAIRE)
    # prompt_data = await read_prompt_data(PROMPT_FILE)
    browser = await playwright.chromium.launch(slow_mo=1000,channel="chrome",headless=False)
    context = await browser.new_context(storage_state="./config/auth.json",
                                        record_video_dir="results/videos/",
                                        record_video_size={"width": 640, "height": 440}
                                        )
    page = await context.new_page()
    await browser.start_tracing(path="results/tracing/trace.json")
    await context.tracing.start(screenshots=True, snapshots=True)
    await page.goto(BASE_URL)
    await page.get_by_text("Login with Google").click()
    await page.locator("button").filter(has_text="Agents").click()
    #test case 1 create agent 
    await page.get_by_role("button", name="Create your agent").click()
    await pic_upload(page,AGENT_PIC,logger)
    await fill_form(page, prompt_data,logger)   
    await page.locator("button").filter(has_text="Agents").click()

    for agent in AGENT_NAME:
        #test upload file
        # await test_upload_file(page,FILE_TO_UPLOAD,DOCUMENT_URL,agent,logger)

        #test add url in document - only 1 URL link in this scope
        # await test_add_url(page,DOCUMENT_URL,agent,logger)
        #test pin agent
        
        await test_pin_agent(page,agent,logger)

        #test continuous chat
        await test_chat_response(page,agent,questionaire,logger)


    await page.screenshot(path="results/videos/pictures/timeout_error_screenshot.png")
    logger.info(json.dumps({"action": "Test completed"}))
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