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
from config.utils import (json_logger, 
                   read_excel_data)
from test_cases.test_pin_agent import test_pin_agent
WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "maya-agent-test.pdf"
PROMPT_FILE = "prompt-template.xlsx"
BASE_URL= "https://azara-ai-dev-server.vercel.app/agents"
TEST_CASE_NAME = "test_add_url"
AGENT_NAME = ['Ava']
DOCUMENT_URL = ['https://doordash.engineering/category/backend/']
async def test_add_url(page,url,agent,logger):
    link = str(url)
    if not isinstance(url, str):
            raise ValueError("URL must be a string")
    try:
        await page.locator('[role="Agent"]').filter(has_text=agent).click()
        await page.locator('[role="MenuList"]').filter(has_text=agent).click()
        await page.locator('[role="menuitem"]').click()
        await page.locator('[role="Tab"]').filter(has_text='Documents').click()
        await page.get_by_role("button", name="Add URL").click()
        
        await page.get_by_placeholder("Enter URL").fill(link)
        await page.get_by_role("button", name="Upload").click()
         # Log success
        logger.info(json.dumps({"result": f"passed{TEST_CASE_NAME}", "detail": "URL added successfully"}))
    except Exception as e:
        logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))