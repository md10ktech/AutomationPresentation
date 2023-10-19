from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pyautogui

# get_node_active_cmd = "cc.director.getScene().getChildByName('Canvas').children[4].children[1].active"
get_score_cmd = ("cc.director.getScene().getChildByName('Canvas').children[4].children[0].children[0]."
                      "getComponent(cc.Label).string")
test_cases = {
    "TestCase_1": False,
    "TestCase_2": False,
    "TestCase_3": False,
    "TestCase_4": False,
    "TestCase_5": False,
    "TestCase_6": False,
}


def clean_log(dirty_log):
    message_list = dirty_log.split()
    message_list.pop(1)
    message_list.pop(0)
    message = " ".join(message_list)
    return message


def get_console_logs():
    console_logs = []
    for console_log in driver.get_log('browser'):
        if console_log['level'] == 'INFO':
            console_log = clean_log(console_log['message'])
            # print(console_log)
            console_logs.append(console_log)
    return console_logs


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://localhost:7456/")

canvas = driver.find_element(By.ID, "GameCanvas")
time.sleep(3)

# Start Test
pyautogui.click(500, 500)
time.sleep(3)

checking = True

normal_interval = 0.8
normal_timelapse = time.time() + normal_interval
rapid_interval = 0.5
rapid_timelapse = time.time() + rapid_interval

# Test Case 1 - No Input
while checking:
    if time.time() > normal_timelapse:
        normal_timelapse = time.time() + normal_interval

        for log in get_console_logs():
            if log.find("Game Over") > 0:
                checking = False
            if log.find("Ground") > 0:
                test_cases["TestCase_1"] = True
                # print(test_cases)

checking = True

# Test Case 2
while checking:
    if time.time() > rapid_timelapse:
        rapid_timelapse = time.time() + rapid_interval
        pyautogui.click(500, 500)

        for log in get_console_logs():
            if log.find("Game Over") > 0:
                checking = False
            if log.find("Sky") > 0:
                test_cases["TestCase_2"] = True
                # print(test_cases)

checking = True

# Test Case 3
while checking:
    if time.time() > rapid_timelapse:
        rapid_timelapse = time.time() + rapid_interval
        canvas.send_keys(Keys.SPACE)

        for log in get_console_logs():
            if log.find("Game Over") > 0:
                checking = False
            if log.find("Sky") > 0:
                test_cases["TestCase_3"] = True

checking = True

# Test Case 4
while checking:
    if time.time() > normal_timelapse:
        normal_timelapse = time.time() + normal_interval
        pyautogui.click(500, 500)

    if time.time() > rapid_timelapse:
        rapid_timelapse = time.time() + rapid_interval
        for log in get_console_logs():
            if log.find("Game Over") > 0:
                checking = False
            if log.find("Pipe") > 0:
                test_cases["TestCase_4"] = True

checking = True

# Test Case 5
while checking:
    if time.time() > normal_timelapse:
        normal_timelapse = time.time() + normal_interval
        canvas.send_keys(Keys.SPACE)

    if time.time() > rapid_timelapse:
        rapid_timelapse = time.time() + rapid_interval
        for log in get_console_logs():
            if log.find("Game Over") > 0:
                checking = False
            if log.find("Pipe") > 0:
                test_cases["TestCase_5"] = True

checking = True

# Test Case 6
while checking:
    if time.time() > normal_timelapse:
        normal_timelapse = time.time() + normal_interval
        # pyautogui.click(500, 500)
        canvas.send_keys(Keys.SPACE)

    if time.time() > rapid_timelapse:
        rapid_timelapse = time.time() + rapid_interval
        for log in get_console_logs():
            if log.find("Passed a pipe!") > 0:
                driver.execute_script(f"console.log({get_score_cmd})")
                for i in get_console_logs():
                    if int(i[1]) > 0:
                        test_cases["TestCase_6"] = True
                        checking = False
                        # TODO: 1. Screenshot 2. Get all logs from start to end. 3. Send report


