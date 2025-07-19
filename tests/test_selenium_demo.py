# tests/test_selenium_demo.py
import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

class TestSeleniumDemo:
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Setup WebDriver based on environment variable"""
        browser = os.getenv('BROWSER', 'chrome').lower()
        
        if browser == 'chrome':
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        elif browser == 'firefox':
            firefox_options = FirefoxOptions()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--width=1920')
            firefox_options.add_argument('--height=1080')
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    def take_screenshot(self, driver, test_name):
        """Take screenshot for debugging"""
        os.makedirs("screenshots", exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"screenshots/{test_name}_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"Screenshot saved: {screenshot_name}")
    
    def test_google_search_success(self, driver):
        """Test Case 1: Successful Google search"""
        try:
            driver.get("https://www.google.com")
            
            # Accept cookies if present
            try:
                accept_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I agree')]"))
                )
                accept_button.click()
            except TimeoutException:
                pass  # No cookie banner found
            
            # Find search box and perform search
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys("Selenium WebDriver GitHub Actions")
            search_box.submit()
            
            # Wait for results
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Verify results are displayed
            results = driver.find_elements(By.CSS_SELECTOR, "h3")
            assert len(results) > 0, "No search results found"
            
            print(f"✅ Found {len(results)} search results")
            
        except Exception as e:
            self.take_screenshot(driver, "google_search_success_failed")
            raise e
    
    def test_invalid_url_error(self, driver):
        """Test Case 2: Intentional error - Invalid URL"""
        try:
            # This will cause a WebDriver error
            driver.get("invalid-url-that-does-not-exist.fake")
            time.sleep(2)
            
            # This assertion should fail if we somehow get here
            assert False, "Should not reach this point with invalid URL"
            
        except Exception as e:
            self.take_screenshot(driver, "invalid_url_error")
            print(f"❌ Expected error occurred: {str(e)}")
            # Re-raise to show the error in test results
            raise e
    
    def test_element_not_found_error(self, driver):
        """Test Case 3: Intentional error - Element not found"""
        try:
            driver.get("https://httpbin.org/html")
            
            # Try to find an element that doesn't exist
            nonexistent_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "this-element-does-not-exist"))
            )
            
            assert False, "Should not find non-existent element"
            
        except TimeoutException as e:
            self.take_screenshot(driver, "element_not_found")
            print(f"❌ Expected TimeoutException: Element not found")
            raise e
        except Exception as e:
            self.take_screenshot(driver, "element_not_found_unexpected")
            raise e
    
    def test_assertion_failure(self, driver):
        """Test Case 4: Intentional error - Assertion failure"""
        try:
            driver.get("https://httpbin.org/html")
            
            # Get the page title
            title = driver.title
            print(f"Actual page title: '{title}'")
            
            # Intentionally wrong assertion
            expected_title = "This Title Does Not Match"
            assert title == expected_title, f"Title mismatch: Expected '{expected_title}', got '{title}'"
            
        except AssertionError as e:
            self.take_screenshot(driver, "assertion_failure")
            print(f"❌ Expected assertion error: {str(e)}")
            raise e
        except Exception as e:
            self.take_screenshot(driver, "assertion_failure_unexpected")
            raise e
    
    def test_slow_page_timeout(self, driver):
        """Test Case 5: Intentional error - Page load timeout"""
        try:
            # Set a very short page load timeout
            driver.set_page_load_timeout(2)
            
            # Try to load a slow page (httpbin delay endpoint)
            driver.get("https://httpbin.org/delay/5")
            
            assert False, "Should timeout before loading"
            
        except Exception as e:
            self.take_screenshot(driver, "page_timeout")
            print(f"❌ Expected timeout error: {str(e)}")
            # Reset timeout for other tests
            driver.set_page_load_timeout(30)
            raise e
    
    def test_form_interaction_success(self, driver):
        """Test Case 6: Successful form interaction"""
        try:
            driver.get("https://httpbin.org/forms/post")
            
            # Fill out the form
            email_field = driver.find_element(By.NAME, "custname")
            email_field.send_keys("test@example.com")
            
            # Submit the form
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            submit_button.click()
            
            # Verify we got to the results page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "pre"))
            )
            
            page_source = driver.page_source
            assert "test@example.com" in page_source, "Form data not found in response"
            
            print("✅ Form submission successful")
            
        except Exception as e:
            self.take_screenshot(driver, "form_interaction_failed")
            raise e

# conftest.py for pytest configuration
import pytest

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "error: marks tests that intentionally produce errors"
    )