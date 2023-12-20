import json
import logging

from functools import lru_cache
import yaml
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from playwright.async_api import TimeoutError,Error

WAIT_TIMEOUT = 0
FILE_TO_UPLOAD = "maya-agent-test.pdf"
PROMPT_FILE = "prompt-template.xlsx"
BASE_URL= "https://azara-ai-dev-server.vercel.app/"
AGENT_PIC = "Maya-agent.jpg"

TEST_CASE_NAME = "utils"

def json_logger():

    logger = logging.getLogger("UAT_test_logger")
    logger.setLevel(logging.INFO)

    # Log formatter - outputs log messages as JSON
    formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')

    # File handler to write logs to a file
    file_handler = logging.FileHandler('results\playwright_test_logs.json')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger



def read_config(file_path):
    """
    Reads and parses a YAML configuration file.

    Args:
    file_path (str): The path to the YAML configuration file.

    Returns:
    dict: A dictionary containing the configuration values.
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def read_excel_data(file_path):
    df = pd.read_excel(file_path,sheet_name=0)
    return df.to_dict(orient="dict")



# def local_load_dotenv(self):
#     ENV_FILE_PATH = BASE_DIR / '.env'
#     if os.getenv('CI', False) is False and ENV_FILE_PATH.exists():
#         load_dotenv(str(ENV_FILE_PATH))


def click_on_button(page, locator):
    try:
        page.wait_for_timeout(1000)
        page.click(locator)
        page.wait_for_timeout(1000)
    except TimeoutError as e:
        print(e)
        logging.error(e)

