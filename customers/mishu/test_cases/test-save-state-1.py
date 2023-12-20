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


WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "maya-agent-test.pdf"
PROMPT_FILE = "prompt-template.xlsx"
BASE_URL= "https://azara-ai-dev-server.vercel.app/"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def json_logger():
    logger = logging.getLogger("UAT_test_logger")
    logger.setLevel(logging.INFO)

    # Log formatter - outputs log messages as JSON
    formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')

    # File handler to write logs to a file
    file_handler = logging.FileHandler('playwright_test_logs.json')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Function to log the result of expect statements


# async def read_prompt_data(file_path):
#     try:
#         # Read the Excel file
#         df = pd.read_excel(file_path)
#         return df.to_dict(orient='records')  # first row contains the header
#     except Exception as e:
#         logger.error(f"Error reading Excel file: {e}")
#         return None


# async def fill_form(page: Page, prompt_data):
#     temp_dict = {}
#     missing_fields = []

#     # Step 1: Check availability of fields and create a temp dictionary
#     for item in prompt_data:
#         field = item['Fields']
#         response = item['Responses']
#         selector = f"textarea[name='{field}']"
#         try:
#             await page.wait_for_selector(selector, state="attached")
#             temp_dict[field] = response
#         except TimeoutError:
#             missing_fields.append(field)
    
#     # Step 2: Error handling for missing fields
#     if missing_fields:
#         missing_fields_str = ', '.join(missing_fields)
#         error_message = f"Error: The following fields are missing on the webpage: {missing_fields_str}"
#         logger.error(error_message)
#         raise ValueError(error_message)

#     # Step 3: Fill in the responses for available fields
#     for field, response in temp_dict.items():
#         try:
#             locator = page.locator(f"textarea[name='{field}']")
#             await locator.click()
#             await locator.fill(response)
#             logger.info(f"Filled field '{field}' with response.")
#         except Exception as e:
#             logger.error(f"Error filling field '{field}': {str(e)}")


# async def create_agent(page, logger):
#     try:
#         await page.get_by_role("button", name="Agents",).click(timeout=0)
#         await page.get_by_role("button", name="Create your agent").click()
#         await expect_call
#         logger.info(json.dumps({"result": "passed", "detail": message}))
#     except Exception as e:
#         logger.error(json.dumps({"result": "failed", "detail": str(e)}))


async def test_upload_file(page, logger):
    try:
        # Wait for and handle the file chooser
        async with page.expect_file_chooser() as fc_info:
            await page.get_by_text("Supported file types: csv, text, pdf, xlsx").click()
        file_chooser = await fc_info.value
        await file_chooser.set_files(FILE_TO_UPLOAD)
        await page.get_by_role("button", name="Upload").click()

        # Log success
        logger.info(json.dumps({"result": "passed", "detail": "File uploaded successfully"}))
    except Exception as e:
        # Log any errors
        logger.error(json.dumps({"result": "failed", "detail": str(e)}))

async def chat_response(page: Page):
    # Locate all agent responses with the class `.output-container`
    # Assuming the agent's chat has a specific identifiable class or attribute
    chat_responses = page.locator(".bg-gray-600 .output-container")
    # chat_responses = page.locator(".output-container:last-of-type")
    # Count the number of chat responses
    count = await chat_responses.count()

    # Ensure there is at least one chat response
    if count == 0:
        raise Exception("No chat responses found.")
   

    # Get the last chat response
    last_chat_response = chat_responses.nth(count - 1)

    # Ensure the last chat response is visible
    await expect(last_chat_response).to_be_visible()

    # Return the text of the last chat response
    return await last_chat_response.inner_text()



async def test_chat_response(page: Page, logger):
    max_retries = 2
    for attempt in range(max_retries):
        try:
            # Send a specific message to the chatbot
            await page.get_by_placeholder("Type your message here...").click()
            await page.fill("input[placeholder='Type your message here...']", "Search the file maya-agent-test.pdf and answer my question. The first question is Do companies in Malaysia require an official stamp or seal?")
            await page.press("input[placeholder='Type your message here...']", "Enter")

            resp = await chat_response(page)
            

            # Check if the response is 50+ characters
            if len(resp) >= 50:
                logger.info(json.dumps({"result": "passed", "detail": "Chat response test passed, response is 50+ characters", "response": resp}))
            else:
                logger.error(json.dumps({"result": "failed", "detail": "Chat response test failed, response is less than 50 characters", "response": resp}))
            break

        except TimeoutError:
            logger.info(f"Timeout occurred, retrying... Attempt {attempt + 1}")
            if attempt < max_retries - 1:
                await page.reload()
            else:
                error_detail = "Agent response timed out after retries."
                logger.error(json.dumps({"result": "failed", "detail": error_detail}))
                return  
            
        except Exception as e:
            logger.error(json.dumps({"result": "failed", "detail": str(e)}))
            if attempt == max_retries - 1:
                raise


            
async def run(playwright: Playwright) -> None:
    logger = json_logger()
    # prompt_data = await read_prompt_data(PROMPT_FILE)
    browser = await playwright.chromium.launch(slow_mo=1000,channel="chrome",headless=False)
    context = await browser.new_context(
        storage_state="auth.json",
        ecord_video_dir="videos/",
        record_video_size={"width": 640, "height": 480})
    
    page = await context.new_page()
    await browser.start_tracing(path="trace.json")
    context.tracing.start(screenshots=True, snapshots=True)
    await page.goto(BASE_URL)
    await page.get_by_text("Login with Google").click()
    await page.get_by_role("button", name="Agents",).click(timeout=0)
    await page.get_by_role("button", name="Create your agent").click()
    # await fill_form(page, prompt_data)
    await page.get_by_role("button", name="Save Agent Info").click()


    #await page.screenshot(path="o.png")

    # await page.locator("input[name=\"name\"]").click()
    await page.locator("textarea[name=\"welcome\"]").click()
    await page.locator("textarea[name=\"welcome\"]").fill("Hello! I'm Maya, your dedicated AI customer service representative. How can I assist you today?")
    await page.locator("input[name=\"name\"]").click()
    await page.locator("input[name=\"name\"]").fill("Maya")
    await page.locator("textarea[name=\"prompt\"]").click()
    await page.locator("textarea[name=\"prompt\"]").fill("Maya's main objective is to answer customer questions taken from uploaded files. Customers interact with Maya primarily in a Q&A format, and she diligently addresses their answers to their questions only from the uploaded files. When she has no knowledge of the questions she needs to respond \" I do not have the knowledge of the questions you asked for\". ")
    await page.locator("input[name=\"role\"]").click()
    await page.locator("input[name=\"role\"]").fill("AI customer service representative")
    await page.locator("textarea[name=\"objective\"]").fill("Maya's mission is to answer customer questions only from the knowledge that was given to her from uploaded files. Every interaction is aimed at ensuring the utmost information accuracy. It's vital that the answers provided are clear, correct, and on-point. In situations where the query is outside her knowledge base, Maya will answer \"I do not have the knowledge of the questions you asked for\". \"")
    await page.locator("textarea[name=\"objective\"]").click()
    await page.locator("#tone").click()
    await page.locator("#tone").fill("Maya communicates in a warm and empathetic tone, prioritizing the needs and feelings of the customer. Her responses are designed to not only provide clear answers but to make the customer feel valued. Throughout every interaction, Ava strives to understand the core concerns of the customer, and her commitment to their satisfaction is unwavering.")
    await page.locator("textarea[name=\"examples\"]").click()
    await page.locator("textarea[name=\"examples\"]").fill("Customer: Can foreign individuals serve as company directors in Malaysia?\nMaya's Answer: Yes. Anyone 18 years old and above (local or foreign) can be a director of the company so long as they fulfill the requirements under the Companies Act 2016.\n\nCustomer: Are companies in Malaysia required to open a domestic bank account?\nMaya's answer: Yes. Companies set up in Malaysia are required to set up a bank account, in which they deposit their minimum share capital to formalise the setup process. MISHU can assist with the bank account opening process.")
    await page.get_by_role("button", name="Save Agent Info").click()
    # await log_expect_result(logger, expect(page.get_by_text("Agent Create Fail")).to_be_visible(), "Fail Agent Create test")
    await page.locator("button").filter(has_text="Agents").click()
    # await page.get_by_role("button", name="Agents").click()
    await page.get_by_text("MaximAI Business ConsultantMaxim's primary objective is to enable users to reali").click()
    await page.get_by_role("button", name="Chat").click()
    # await page.get_by_role("button", name="Files 0").click(timeout=WAIT_TIMEOUT)

    # await test_upload_file(page, logger)
    await test_chat_response(page, logger)
    
    
    logger.info(json.dumps({"action": "Test completed"}))
    # ---------------------
    browser.stop_tracing()
    context.tracing.stop(path="video/trace1.zip")
    await context.storage_state(path="auth.json")
    # await context.close()
    # await browser.close()
    # await playwright.dispose()
    

async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
