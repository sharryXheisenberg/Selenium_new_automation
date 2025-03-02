from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from collections import namedtuple

class BrowserHandler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get("https://app-staging.nokodr.com/")

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def locate_element(self, locator, timeout=10, clickable=False):
        wait = WebDriverWait(self.driver, timeout)
        condition = EC.element_to_be_clickable if clickable else EC.presence_of_element_located
        return wait.until(condition(locator))

    def navigate_to_signup(self):
        signup_btn = self.locate_element((By.LINK_TEXT, "Sign up"), clickable=True)
        signup_btn.click()

    def input_signup_details(self, email, agree_terms=True):
        email_field = self.locate_element(
            (By.XPATH, "(//input[@class='slds-input ng-untouched ng-pristine ng-valid'])[3]")
        )
        email_field.clear()
        email_field.send_keys(email)

        if agree_terms:
            terms_checkbox = self.locate_element((By.CLASS_NAME, "slds-checkbox__label"), clickable=True)
            terms_checkbox.click()

    def submit_form(self):
        submit_btn = self.locate_element(
            (By.XPATH, "//div[@class='slds-col slds-size_1-of-1']"), clickable=True
        )
        submit_btn.click()

    def validate_success(self, expected_text):
        try:
            success_msg = self.locate_element((By.XPATH, "//*[contains(text(),'OTP')]") )
            actual_text = success_msg.text
            if expected_text in actual_text:
                print(f"Success: Found '{expected_text}' in message")
            else:
                print(f"Failure: Expected '{expected_text}', but got '{actual_text}'")
        except TimeoutException:
            print("Failure: Success message did not appear within the time limit")

    def validate_error(self, expected_error):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'OTP')]") )
            )
            print(f"Error: Success message appeared when expecting error '{expected_error}'")
        except TimeoutException:
            error_msgs = self.driver.find_elements(By.CLASS_NAME, "error-message")
            errors = [err.text for err in error_msgs if err.text]
            if any(expected_error in err for err in errors):
                print(f"Error Check Passed: Found '{expected_error}' in error messages")
            else:
                print(f"Error Check Failed: Expected '{expected_error}', but found {errors or 'no errors'}")

class SignupAutomation:
    def run_test(self, email, terms_agreed, test_type, expected_result):
        handler = BrowserHandler()
        try:
            handler.navigate_to_signup()
            handler.input_signup_details(email, terms_agreed)
            handler.submit_form()

            if test_type == "success":
                handler.validate_success(expected_result)
            elif test_type == "error":
                handler.validate_error(expected_result)
        except Exception as e:
            print(f"Test encountered an error: {e}")
        finally:
            handler.close_browser()

TestCase = namedtuple('TestCase', ['name', 'email', 'terms_agreed', 'test_type', 'expected_result'])

test_cases = [
    TestCase(
        name="Successful Signup",
        email="valid.email@example.com",
        terms_agreed=True,
        test_type="success",
        expected_result="OTP"
    ),
    TestCase(
        name="Invalid Email Format",
        email="invalid-email",
        terms_agreed=True,
        test_type="error",
        expected_result="Invalid email format"
    ),
    TestCase(
        name="Missing Email",
        email="",
        terms_agreed=True,
        test_type="error",
        expected_result="Email is required"
    ),
    TestCase(
        name="Terms Not Accepted",
        email="valid.email@example.com",
        terms_agreed=False,
        test_type="error",
        expected_result="You must accept the terms and conditions"
    )
]

if __name__ == "__main__":
    tester = SignupAutomation()
    for case in test_cases:
        print(f"\nRunning test: {case.name}...")
        tester.run_test(
            email=case.email,
            terms_agreed=case.terms_agreed,
            test_type=case.test_type,
            expected_result=case.expected_result
        )
