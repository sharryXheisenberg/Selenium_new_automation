from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowserManager:
    browser_instance = None

    @classmethod
    def initialize(cls):
        cls.browser_instance = webdriver.Chrome()
        cls.browser_instance.maximize_window()
        cls.browser_instance.implicitly_wait(10)
        cls.browser_instance.get("https://app-staging.nokodr.com/")

    @classmethod
    def close_browser(cls):
        if cls.browser_instance:
            cls.browser_instance.quit()

    @classmethod
    def perform_signup(cls):
        wait = WebDriverWait(cls.browser_instance, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//input[contains(@class, 'slds-input')])[3]")))
        wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "slds-checkbox__label"))).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='slds-col slds-size_1-of-1']"))).click()

class UserAuthPage(BrowserManager):

    @classmethod
    def authenticate_user(cls, user_email, user_password):
        cls.initialize()
        email_input = user_email.strip()
        password_input = user_password.strip()

        wait = WebDriverWait(cls.browser_instance, 10)
        email_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@name='username']")))
        password_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@name='password']")))
        
        email_box.send_keys(email_input)
        password_box.send_keys(password_input)
        
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@title='Log In']"))).click()

        try:
            error_msg = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='content-margin']")))
            message_text = error_msg.text
            if "Invalid Email or Password" in message_text:
                print(f"❌ Authentication failed for {email_input}: Invalid credentials.")
            elif "Please enter a valid email" in message_text:
                print(f"❌ Authentication failed for {email_input}: Incorrect email format.")
            else:
                print(f"❌ Unexpected error during authentication for {email_input}: {message_text}")
        except Exception:
            print(f"✅ Authentication successful for {email_input}!")
        finally:
            cls.close_browser()

if __name__ == "__main__":
    # Sample test cases
    login_cases = [
        ("john.doe@gmail.com", "JohnDoe@123"),
        ("pandesaurabh4596@gmail.com", "Pass@1234"),
        ("user@example.com", "password123")
    ]

    for email, password in login_cases:
        print(f"\n🔍 Running authentication test: Email: '{email}', Password: '{password}'")
        UserAuthPage.authenticate_user(email, password)
