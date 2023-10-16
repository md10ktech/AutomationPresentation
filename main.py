from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(3)
english = driver.find_element(By.ID, "langSelect-EN")
english.click()

time.sleep(5)
cookie = driver.find_element(By.ID, "bigCookie")

buyTime = time.time() + 5
upgradeTime = time.time() + 5

isClicking = True

while isClicking:
    cookie.click()

    if time.time() > buyTime:
        buyTime = time.time() + 1

        cursorUnlocked = driver.find_element(By.XPATH, "//*[@id='product0']")
        cursorUnlocked.click()

        numOfCursor = driver.find_element(By.ID, "productOwned0")

        if numOfCursor.text == "30":
            driver.get_screenshot_as_file("result.png")
            isClicking = False

    if time.time() > upgradeTime:
        upgradeTime = time.time() + 5
        try:
            upgrade = driver.find_element(By.XPATH, "//*[@id='upgrade0']")
            upgrade.click()
        except NoSuchElementException:
            pass

