import pytest
from selenium import webdriver

from selenium.webdriver.firefox.service import Service as Firefox_Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    """
    setup of browser, to be passed in for each ui test
    """
    # setup
    options = Options()
    options.headless = True
    s = Firefox_Service(GeckoDriverManager().install())
    browser = webdriver.Firefox(service=s, options=options)

    # return when completed
    yield browser

    # tear down
    browser.close()

def test_ui(browser):
    """
    enter search term and assert next page
    """
    input_text = 'test'
    # setup
    wait = WebDriverWait(browser, 10)
    browser.get("http://localhost:80")
    
    # act
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchterm"]')))
    element = browser.find_element(By.XPATH, '//*[@id="searchterm"]')
    element.send_keys(input_text)
    element = browser.find_element(By.XPATH, '/html/body/form/input[2]')
    element.click()

    # assert
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/a')))
    result = browser.find_element(By.XPATH, '/html/body')

    assert input_text in result.text