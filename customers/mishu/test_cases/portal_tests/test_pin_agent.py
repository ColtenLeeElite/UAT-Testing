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
WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "maya-agent-test.pdf"
PROMPT_FILE = "prompt-template.xlsx"
BASE_URL= "https://azara-ai-dev-server.vercel.app/agents"
TEST_CASE_NAME = "PIN_AGENT"
async def test_pin_agent(page,agent,logger):
    try:
        await page.locator('[role="Agent"]').filter(has_text=agent).click()
        await page.locator('[role="Pin"]').filter(has_text=agent).click()
        logger.info(json.dumps({"result": f"passed{TEST_CASE_NAME}", "detail": "Pin successfully"}))
    except Exception as e:
        logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))
  