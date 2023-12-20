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
#                    read_excel_data)
WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "maya-agent-test.pdf"
PROMPT_FILE = "prompt-template.xlsx"
BASE_URL = "https://azara-ai-dev-server.vercel.app/"
TEST_CASE_NAME = "test_create_agent"
AGENT_PIC = "Maya-agent.jpg"
QUESTIONAIRE = "Mishu_question_answer_pairs.xlsx"

# CLIENT_FILE_PATH = "./Mishu_files"


async def fill_form(page, prompt_data):
    # change directory
    # os.chdir(CLIENT_FILE_PATH)
    element_mapping = {
        "Agent name": "input[name=\"name\"]",
        "Welcome Message": "textarea[name=\"welcome\"]",
        # "Prompt": "textarea[name=\"prompt\"]",
        "Role": "input[name=\"role\"]",
        "Objective": "textarea[name=\"objective\"]",
        "Tone": "textarea[name=\"tone\"]",
        "Examples": "textarea[name=\"examples\"]"
    }
    response = prompt_data['Responses'].values()
    agent_name = prompt_data['Responses'][0]
    element_pairs = dict(zip(element_mapping.values(), response))
    for k, v in element_pairs.items():
        await page.locator(k).click()
        await page.locator(k).fill(v)
    await page.get_by_role("button", name="Save Agent Info").click()
    try:
        # await expect(page.get_by_text("Agent Create Sucess")).to_be_visible()
        await page.locator("button").filter(has_text="Agents").click()
        expect(page.locator('[role="Agent"]').filter(has_text=agent_name))
        # logger.info(json.dumps(
        #     {"result": f"passed{TEST_CASE_NAME}", "detail": "prompt passed successfully"}))
    except AssertionError as a:
        print('')
        # logger.error(json.dumps(
        #     {"result": f"failed{TEST_CASE_NAME}", "detail": str(a)}))

    except Exception as e:

        print('')
        # Log any errors
        # logger.error(json.dumps(
        #     {"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))


async def pic_upload(page, AGENT_PIC):
    # os.chdir(CLIENT_FILE_PATH)
    try:
        # Wait for and handle the file chooser
        async with page.expect_file_chooser() as fc_info:
            await page.locator("input[type=\"file\"]").click()
        file_chooser = await fc_info.value
        await file_chooser.set_files(AGENT_PIC)
        await page.locator("input[type=\"file\"]").click()

    except Exception as e:
        # Log any errors
        # logger.error(json.dumps(
        #     {"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))
        print('')


# async def run(playwright: Playwright) -> None:
#     logger = json_logger()
#     prompt_data = read_excel_data(PROMPT_FILE)
#     questionaire = read_excel_data(QUESTIONAIRE)
#     # prompt_data = await read_prompt_data(PROMPT_FILE)
#     browser = await playwright.chromium.launch(slow_mo=1000,channel="chrome",headless=False)
#     context = await browser.new_context(storage_state="auth.json",
#                                         record_video_dir="results/videos/",
#                                         record_video_size={"width": 240, "height": 140}
#                                         )
#     page = await context.new_page()
#     await browser.start_tracing(path="results/tracing/trace.json")
#     await context.tracing.start(screenshots=True, snapshots=True)
#     await page.goto(BASE_URL)
#     await page.get_by_text("Login with Google").click()
#     await page.locator("button").filter(has_text="Agents").click()
#     #test case 1 create agent
#     await page.get_by_role("button", name="Create your agent").click()
#     await pic_upload(page,AGENT_PIC,logger)
#     await fill_form(page, prompt_data,logger)
#     await page.locator("button").filter(has_text="Agents").click()


#     # ---------------------
#     browser.stop_tracing()
#     await context.tracing.stop(path="results/tracing/trace1.zip")
#     await context.storage_state(path="auth.json")
#     # await context.close()
#     # await browser.close()


# async def main() -> None:
#     async with async_playwright() as playwright:
#         await run(playwright)


# asyncio.run(main())
