import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO)

class WebDriverController:
    driver_instance = None

    @staticmethod
    def start_browser():
        """Launch WebDriver and open the target website."""
        WebDriverController.driver_instance = webdriver.Chrome()
        WebDriverController.driver_instance.maximize_window()
        WebDriverController.driver_instance.get("https://app-staging.nokodr.com/")

    @staticmethod
    def close_browser():
        """Terminate the browser session."""
        if WebDriverController.driver_instance:
            WebDriverController.driver_instance.quit()

class PasswordResetTest(WebDriverController):

    @staticmethod
    def access_reset_page():
        """Navigate to the password reset page."""
        WebDriverController.driver_instance.get("https://app-staging.nokodr.com/")
        wait = WebDriverWait(WebDriverController.driver_instance, 10)
        forgot_password_link = (By.LINK_TEXT, "Forgot Password?")
        wait.until(EC.element_to_be_clickable(forgot_password_link)).click()
        wait.until(EC.presence_of_element_located((By.ID, "email")))

    @staticmethod
    def validate_empty_email():
        logging.info("Checking validation for empty email field...")
        wait = WebDriverWait(WebDriverController.driver_instance, 10)
        proceed_btn = (By.XPATH, "//div[@title='Proceed']")
        wait.until(EC.element_to_be_clickable(proceed_btn)).click()
        try:
            error_msg_locator = (By.XPATH, "//div[contains(@class, 'MuiFormHelperText-root') and contains(@class, 'Mui-error')]")
            error_msg_element = wait.until(EC.visibility_of_element_located(error_msg_locator))
            error_text = error_msg_element.text
            assert "Please enter email" in error_text, f"Validation failed! Expected message: 'Please enter email', but found: '{error_text}'"
            logging.info("Empty email validation passed.")
        except TimeoutException:
            logging.error("Empty email validation failed. No error message detected!")

if __name__ == "__main__":
    try:
        WebDriverController.start_browser()
        PasswordResetTest.access_reset_page()
        PasswordResetTest.validate_empty_email()
    except Exception as error:
        logging.error(f"Test execution encountered an error: {error}")
    finally:
        WebDriverController.close_browser()
