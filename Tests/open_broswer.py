from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


driver.get("https://app-staging.nokodr.com/")

time.sleep(5)

driver.quit()