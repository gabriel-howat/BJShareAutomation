from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.remote_connection import LOGGER
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService # Similar thing for firefox also!
from subprocess import CREATE_NO_WINDOW
import logging
import time


url = "https://bj-share.info/index.php"
login_url = "https://bj-share.info/login.php?c"

def open_login():

    driver_path = "C:\Program Files\ChromeDev\chrome-win64"
# Create a new instance of the browser driver
    chrome_options = Options()
    chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Optional

#    LOGGER.setLevel(logging.ERROR)
    # Specify the ChromeDriver executable path in options
    chrome_options.add_argument("webdriver.chrome.driver=" + driver_path)
    #chrome_options.add_argument("---headless")
    #chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #chrome_options.add_argument("--log-level=3")
    #chrome_options.add_argument("start-maximized")
    
    #chrome_service = ChromeService(ChromeDriverManager().install())
    
    #chrome_service.creationflags = CREATE_NO_WINDOW
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(login_url)

    wait = WebDriverWait(driver, 90)

    wait.until(EC.url_to_be(login_url))

    current_url = driver.current_url

    if current_url == login_url:
        print("Login page loaded successfully")

        # Perform login actions (fill in credentials, click login button, etc.)
        # ...

        # Wait for the URL to change after successful login
        wait_for_url_change(driver, current_url)

        # URL has changed, indicating successful login
        print("Login successful")
        return driver

    else:
        print("Login page did not load")


def wait_for_url_change(driver, current_url):
    def url_has_changed(driver):
        return driver.current_url != current_url

    try:
        WebDriverWait(driver, 999).until(EC.url_to_be(url))
    except TimeoutException:
        print("Timeout: URL did not change")