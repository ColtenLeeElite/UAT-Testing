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



async def whatsapp_response(page,logger):
    try:
        messages_locator = "div.copyable-text[data-pre-plain-text*='27/11/2023'] >> span._11JPr.selectable-text.copyable-text >> span:last-child"
        count = await page.locator(messages_locator).count()
        print("Number of messages:", count)

        messages =[]
        for i in range(count):
            text = await page.locator(messages_locator).nth(i).text_content()
            messages.append(text)
 

        # last_message_selector = "div.copyable-text[data-pre-plain-text*='Smith Security']"
        # messages = f"div.copyable-text[data-pre-plain-text*='{date}'][data-pre-plain-text*='{WHATSAPP_CONTACT}'] >> nth=-2"
        # Ensure the selector is present in the DOM
        # await page.wait_for_selector(last_message_selector)
        # Retrieve the text of the last message
        # last_message_selector = await page.query_selector_all(messages) 
        # last_message_selector = await page.locator(messages).text_content()


        df = pd.DataFrame({'Messages': messages})
        df.to_excel('./results/continuous_whatsapp_response_test.xlsx', index=False)
        logger.info(json.dumps({"result": f"passed{TEST_CASE_NAME}", "detail": "response is 20+ characters", "response": str(select_date)}))
        
    except Exception as e:
            logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))
            raise e
    
    
    
    # whatsapp_resp = await page.inner_text(last_message_selector)
    # # Return the text of the last chat response
    # await whatsapp_resp.wait_for(state="visible",timeout=WAIT_TIMEOUT)
    # return await whatsapp_resp.inner_text()

async def test_whatsapp_response(page,questionaire,logger):
    questions = questionaire['Questions'].items()
    answers_list = []
    asked_questions = []
    timeout_error_count = 0
    max_timeout_errors = 5
    
    for question in questions:
        try:
            await page.get_by_role("textbox", name="Type a message").get_by_role("paragraph").click()
            await page.get_by_role("textbox", name="Type a message").fill(f"{question}")
            await page.get_by_label("Send").click()
            await asyncio.sleep(10)
            asked_questions.append(question)
            await asyncio.sleep(10)
            resp = await whatsapp_response(page)
            answers_list.append(resp)
            
            # Check if the response is 50+ characters
            if len(resp) >= 20:
                logger.info(json.dumps({"result": f"passed{TEST_CASE_NAME}", "detail": "response is 20+ characters", "response": resp}))
            else:
                logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": "response is <20 characters", "response": resp}))
            
        except Exception as e:
            logger.error(json.dumps({"result": f"failed{TEST_CASE_NAME}", "detail": str(e)}))
            timeout_error_count+=1
            if timeout_error_count >= max_timeout_errors:
                # Take a screenshot when the condition is met
                print("Exceeded maximum timeout errors. Test stopped.")
                break


    qna_list = list(zip(asked_questions,answers_list))
    df_input = pd.DataFrame(qna_list,columns=['Questions','Responses'])
    try:
        df_input.to_excel('./results/continuous_whatsapp_response_test.xlsx', index=False)
    except Exception as e:
        print("Error writing to Excel:", e)
    