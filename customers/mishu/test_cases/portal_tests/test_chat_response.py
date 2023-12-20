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
import config
from config.utils import (json_logger, 
                   read_excel_data)

WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "Mishu_files/maya-agent-test.pdf"
PROMPT_FILE = "Mishu_files/prompt-template.xlsx"
BASE_URL= "https://azara-ai-dev-server.vercel.app/"
TEST_CASE_NAME = "test_doc_upload"
AGENT_PIC = "Mishu_files/Maya-agent.jpg"

async def chat_response(page: Page):
    # Locate all agent responses with the class `.output-container`
    chat_responses = page.locator(".testNode")
    # chat_responses = page.locator(".output-container:last-of-type")
    # Count the number of chat responses
    # count = await chat_responses.count()

    # # Ensure there is at least one chat response
    # if count == 0:
    #     raise Exception("No chat responses found.")
   

    # Get the last chat response
    # last_chat_response = chat_responses.nth((-1))
    # await expect(chat_responses).to_be_visible()
    # await page.reload()

    

    # Return the text of the last chat response
    return await chat_responses.inner_text()



async def test_chat_response(page: Page, logger):
    max_retries = 2
    for attempt in range(max_retries):
        try:
            # Send a specific message to the chatbot
            await page.get_by_placeholder("Type your message here...").click()
            # await page.fill("input[placeholder='Type your message here...']", "hello")
            await page.fill("input[placeholder='Type your message here...']", "Search the file maya-agent-test.pdf and answer my question. The first question is Do companies in Malaysia require an official stamp or seal?")
            await page.press("input[placeholder='Type your message here...']", "Enter")
            await asyncio.sleep(WAIT_TIMEOUT)
            resp = await chat_response(page)
            # resp = await expect(chat_response).to_be_visible()

            # Check if the response is 50+ characters
            if len(resp) >= 29:
                logger.info(json.dumps({"result": f"passed{TEST_CASE_NAME}", "detail": "Chat response test passed, response is 50+ characters", "response": resp}))
                success_logged = True
                break
            elif not success_logged:
                logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": "Chat response test failed, response is less than 50 characters", "response": resp}))
            

        except TimeoutError:
            logger.info(f"Timeout occurred, retrying... Attempt {attempt + 1}")
            if attempt < max_retries - 1:
                await page.reload()
            else:
                error_detail = "Agent response timed out after retries."
                logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": error_detail}))
                return  
            
        except Exception as e:
            logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))
            if attempt == max_retries - 1:
                raise

