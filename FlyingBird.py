from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

# dc = DesiredCapabilities.CHROME
# dc['goog:loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://localhost:7456/")

canvas = driver.find_element(By.ID, "GameCanvas")

time.sleep(3)

flyInterval = time.time() + 0.5

isClicking = True

while isClicking:
    if time.time() > flyInterval:
        flyInterval = time.time() + 0.5
        canvas.send_keys(Keys.SPACE)

        for entry in driver.get_log('browser'):
            if(entry['level'] == "INFO"):
                print(entry['message'])
                # ^ Need to clean