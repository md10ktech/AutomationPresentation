from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.actions.action_builder import ActionBuilder
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as cond
import pyautogui
import time
import TestReport as test_report

clicks = 15
click_increment = 3


def click_candy(num_of_clicks):
    # pyautogui.moveTo(300, 500)
    for step in range(num_of_clicks):
        pyautogui.mouseDown(300, 500)
        pyautogui.mouseUp()


def increase_clicks():
    global clicks, click_increment
    clicks += click_increment
    click_increment += 1
    print(f"Clicks : {clicks}")
    return clicks


def buy_autoclick():
    pyautogui.moveTo(700, 350)
    pyautogui.mouseDown()
    pyautogui.mouseUp()


def buy_cursor():
    pyautogui.moveTo(700, 420)
    pyautogui.mouseDown()
    pyautogui.mouseUp()


def make_more_candy():
    pyautogui.moveTo(600, 250)
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    pyautogui.moveTo(765, 465)
    pyautogui.mouseDown()
    pyautogui.mouseUp()


def send_test_result():
    driver.get_screenshot_as_file("result.png")
    time.sleep(1)
    test_report.write_report("Candy Clicker Test")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://cookieclicker2.io/candy-clicker-2")

time.sleep(3)

playbox = driver.find_element(By.CLASS_NAME, 'play-box')
playbox.click()

# expand = driver.find_element(By.ID, 'expand')
# expand.click()

driver.execute_script("return arguments[0].scrollIntoView(true);", playbox)
time.sleep(1)

# Bonus button - 100, 380
# pyautogui.click(clicks=5, interval=1) # <- DOES NOT WORK!
# pyautogui.doubleClick()

click_candy(clicks)
time.sleep(1)

for i in range(5):
    buy_autoclick()
    click_candy(increase_clicks())

for i in range(2):
    buy_cursor()
    click_candy(clicks)

make_more_candy()
click_candy(5)
send_test_result()

# wait = WebDriverWait(driver, 10)
# try:
#     canvas = wait.until(
#         cond.presence_of_element_located((By.CLASS_NAME, 'game-play'))
#     )
# finally:
#     print("Cannot find 'app' ID element.")

# action = ActionBuilder(driver)
# action.pointer_action.move_to_location(300, 500)
# action.pointer_action.click()
# action.perform()

# ActionChains(driver)\
#     .move_to_element_with_offset(playbox, -100, 0)\
#     .click()\
#     .perform()
