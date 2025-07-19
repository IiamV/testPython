# File: tests/test_demo.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pytest

# Set up Chrome options for headless mode (suitable for GitHub Actions)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Test 1: Successful login (should pass)
def test_successful_login():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.saucedemo.com")
    
    # Enter valid credentials
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Verify successful login by checking for inventory page
    assert "inventory.html" in driver.current_url, "Login failed!"
    driver.quit()

# Test 2: Invalid login (should fail to demonstrate error detection)
def test_invalid_login():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.saucedemo.com")
    
    # Enter invalid credentials
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    
    # Verify error message is displayed
    error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "Username and password do not match" in error_message, "Error message not detected!"
    driver.quit()

# Test 3: Check for UI element (demonstrate UI validation)
def test_check_ui_element():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.saucedemo.com")
    
    # Verify login button is present
    login_button = driver.find_element(By.ID, "login-button")
    assert login_button.is_displayed(), "Login button not found!"
    driver.quit()
