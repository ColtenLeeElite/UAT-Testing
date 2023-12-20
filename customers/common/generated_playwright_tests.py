from playwright.sync_api import sync_playwright

BASE_URL = "http://0.0.0.0:9000"

def test_flow_1(page):
    """
    Test Flow 1: Test the deployed model with a valid input
    """
    headers = {"Content-Type": "application/json"}
    data = """
    {
        "input" : "IMEI: 867442050433701",
        "agent_name" : "Farah",
        "email_subject" : "testing"
    }
    """
    response = page.request.post(f"{BASE_URL}/query/deployed/1", headers=headers, data=data)
    assert response.ok, f"Request failed: {BASE_URL}/query/deployed/1"

def test_flow_2(page):
    """
    Test Flow 2: Test the deployed model with an empty input
    """
    headers = {"Content-Type": "application/json"}
    data = """
    {
        "input" : "",
        "agent_name" : "Farah",
        "email_subject" : "testing"
    }
    """
    response = page.request.post(f"{BASE_URL}/query/deployed/1", headers=headers, data=data)
    assert response.ok, f"Request failed: {BASE_URL}/query/deployed/1}"

def test_flow_3(page):
    """
    Test Flow 3: Test the deployed model with a valid input
    """
    headers = {"Content-Type": "application/json"}
    data = """
    {
        "input" : "123 Elmwood Ave Springfield, IL 62704, 0129348123123",
        "agent_name" : "Farah",
        "email_subject" : "I am John"
    }
    """
    response = page.request.post(f"{BASE_URL}/query/deployed/1", headers=headers, data=data)
    assert response.ok, f"Request failed: {BASE_URL}/query/deployed/1}"

def test_flow_4(page):
    """
    Test Flow 4: Test the deployed model with an empty input
    """
    headers = {"Content-Type": "application/json"}
    data = """
    {
        "input" : "",
        "agent_name" : "Farah",
        "email_subject" : "testing"
    }
    """
    response = page.request.post(f"{BASE_URL}/query/deployed/1", headers=headers, data=data)
    assert response.ok, f"Request failed: {BASE_URL}/query/deployed/1}"
