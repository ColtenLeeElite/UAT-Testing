# UAT Testing

This repository contains User Acceptance Testing (UAT) Playwright tests, organized by folder per customer. These tests can be run manually or as part of Continuous Integration/Continuous Deployment (CI/CD) pipelines or merge requests to prevent breaking the build. Test results will be placed into the README of the relevant branch being tested.

## Introduction

The structure of the repository:

- **Customer/common/get_start**:
  - `starter_script.py`: Helps you get started with Playwright.
  - `TestCaseBuilder-Mishu.xls`: A sample test case builder to align what needs to be tested.

- **mishu**: Related UAT tests for Mishu customers include:
  The folder contains the below main files
  - `playwright_test_logs.json`: Log result of the test.
  - `requirements.txt`: Requirements to run Playwright for testing.
  - `auth.json`: This file is not uploaded to GitHub. It is produced when you first run codegen to login at `playwright codegen azara-ai-dev-server.vercel.app --save-storage=auth.json`. To obtain a login for the Gmail testing account, please reach out to Prem.
  - `playwright_test_run.py`: is the main script for running UAT test cases that has chained together. It reads test cases from the folder test_cases. For the script to run you need auth.json and  all the agent's pictures, and files that need to be uploaded files, and for the test cases to read from to be in the same directory for proper execution.

  The folder contains the below main folders
  -  `Config` folder:  store config files for test cases to read from including the `utils.py` file. It is subject for future development of wrapper, logging, and path configuration
  -  `results` folder: logging result include tracing, video, screenshot . Video and tracing is already implemented. Screenshot must be manually implemented per step needed . in the folder `results` there is  `playwright_test_logs.json` that Log result of the test.
  -  `test_cases`: modularize test actions that you can run individually or chain in cases in `playwright_test_run.py`. To run each case one by one you need to copy from `asynd def run` to the end from the file  `playwright_test_run.py`
 
## How to run the tests 
### Prerequisites
Ensure you have the following installed:
- Python 3.7 or later
- Playwright for Python
- All dependencies listed in `requirements.txt`

### Running E2E Mishu testing from `playwright_test_run.py` for azara portal testing
1. Clone the repository to your local machine.
2. Navigate to the Mishu folder.
3. Install the required dependencies using the following command: pip install -r requirements.txt
4. Make sure you have the `auth.json` file in the Mishu folder. This is necessary for authentication during the tests.
5. Make sure you have files that need for uploaded and read for the test cases. For Mishu's case here are the files needed
    - `Mishu_question_answer_pairs.xlsx` contains a list of questions to parse to the agent
    - `Maya-agent.JPG` picture to upload to agent
    - `prompt-template.xlsx` template to fill in prompt agent
    - `requirements.txt` dependencies
  
6. Execute the following command to run the Playwright test script: `python playwright_test_run.py`. This script will perform the UAT tests as defined and log the results in `playwright_test_logs.json`.
7. At the beginning of the script `playwright_test_run.py`  there are global variables that you could edit to choose the server to test, agent, and timeout eg.In the next milestone this will be move to read from env variables
   

### Note
For  reading  on each test case scope, features, pending and known errors you must visit the below pages
  - https://www.notion.so/blackboxai/Milestone-1-for-1st-Test-Cases-b2ace69a29cf4a08bb77bffe56bc765e
  - https://www.notion.so/blackboxai/Milestone-2-test-Whatsapp-chat-and-Widget-c2aff5e8614349909c8fa1f7116c795a

