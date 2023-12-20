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

WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "maya-agent-test.pdf"
PROMPT_FILE = "prompt-template.xlsx"
BASE_URL= "https://azara-ai-dev-server.vercel.app/"
AGENT_PIC = "Maya-agent.jpg"

TEST_CASE_NAME = "continuous_response_test"


async def chat_response(page,logger):
    try:
        # Wait for the chat response to appear
        await page.locator(".testNode").wait_for(state="visible",timeout=WAIT_TIMEOUT)
        # Get the chat response element
        chat_response = page.locator(".testNode")
        # Return the text of the chat response
        return await chat_response.inner_text()

    except Exception as e:
            logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))
            raise e

async def test_chat_response(page,agent,questionaire,logger):
    await page.locator('[role="Agent"]').filter(has_text=agent).click()
    await page.get_by_role("button", name="Chat").click()
    questions = questionaire['Questions'].items()
    answers_list = []
    asked_questions = []
    timeout_error_count = 0
    max_timeout_errors = 5
    
    for question in questions:
        try:
            await page.locator("input[placeholder='Type your message here...']").click()
            await page.locator("input[placeholder='Type your message here...']").fill(f"{question}")
            await page.locator("input[placeholder='Type your message here...']").press("Enter")
            asked_questions.append(question)
            resp = await chat_response(page)
            answers_list.append(resp)
            
            # Check if the response is 50+ characters
            if len(resp) >= 20:
                logger.info(json.dumps({"result": f"passed{TEST_CASE_NAME}", "detail": "response is 20+ characters", "response": resp}))
            else:
                logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": "response is <20 characters", "response": resp}))
            
        except Exception as e:
            logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))
            timeout_error_count+=1
            logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": "display error need to reload the page to get next question"}))
            await page.reload()
            if timeout_error_count >= max_timeout_errors:
                # Take a screenshot when the condition is met
                print("Exceeded maximum timeout errors. Test stopped.")
                break


    qna_list = list(zip(asked_questions,answers_list))
    df_input = pd.DataFrame(qna_list,columns=['Questions','Responses'])
    try:
        df_input.to_excel('./results/continuous_agent_response_test.xlsx', index=False)
    except Exception as e:
        print("Error writing to Excel:", e)


