import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# SonarQube will catch these issues:
password = "hardcoded_password_123"  # Security: Hardcoded credentials
api_key = "sk-1234567890abcdef"      # Security: Hardcoded API key

def login_user(username, pwd):
    # Code smell: Unused variable
    unused_var = "this is never used"
    
    # Bug: Potential null pointer
    if username:
        print("Username: " + username)
    print("Password: " + pwd)  # This could be None
    
    # Code smell: Dead code
    return True
    print("This line will never execute")

def bad_exception_handling():
    try:
        result = 10 / 0
    except:  # Code smell: Broad exception catching
        pass  # Code smell: Empty catch block

def inefficient_loop():
    items = []
    # Performance: Inefficient list building
    for i in range(1000):
        items = items + [i]  # Should use append()
    return items

# Selenium will catch these issues:
def selenium_test():
    driver = webdriver.Chrome()
    
    try:
        # Bad practice: Hardcoded waits
        time.sleep(5)  # Instead of explicit waits
        
        # Selenium issue: Fragile locator
        element = driver.find_element(By.XPATH, "//div[1]/span[2]/a[3]")
        
        # Missing wait - element might not be ready
        element.click()
        
        # Another hardcoded wait
        time.sleep(3)
        
        # Fragile locator by index
        button = driver.find_element(By.CSS_SELECTOR, "button:nth-child(5)")
        button.click()
        
    except Exception as e:
        # Poor error handling
        print("Something went wrong")
        
    # Resource leak: Driver not properly closed
    # driver.quit() is missing

# More SonarQube issues:
def duplicate_code_1():
    print("Processing data...")
    data = [1, 2, 3, 4, 5]
    total = 0
    for item in data:
        total += item
    print(f"Total: {total}")
    return total

def duplicate_code_2():
    print("Processing data...")  # Duplicate code
    data = [6, 7, 8, 9, 10]
    total = 0
    for item in data:           # Duplicate logic
        total += item
    print(f"Total: {total}")    # Duplicate code
    return total

# Cognitive complexity issue
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                if x > y:
                    if y > z:
                        if x > z:
                            return "very complex"
                        else:
                            return "still complex"
                    else:
                        return "complex"
                else:
                    return "also complex"
            else:
                return "negative z"
        else:
            return "negative y"
    else:
        return "negative x"

if __name__ == "__main__":
    login_user("admin", password)
    bad_exception_handling()
    inefficient_loop()
    selenium_test()
    duplicate_code_1()
    duplicate_code_2()
    complex_function(1, 2, 3)
