from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime as dt
import pyautogui
import TestReport as test_report

# get_node_active_cmd = "cc.director.getScene().getChildByName('Canvas').children[4].children[1].active"
get_score_cmd = ("cc.director.getScene().getChildByName('Canvas').children[4].children[0].children[0]."
                 "getComponent(cc.Label).string")

logs = []

pass_text = "✔ PASS"
fail_text = "✘ FAIL"

test_cases = {
    "TestCase_1": fail_text,
    "TestCase_2": fail_text,
    "TestCase_3": fail_text,
    "TestCase_4": fail_text,
    "TestCase_5": fail_text,
    "TestCase_6": fail_text,
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
            console_logs.append(console_log)

    # print(console_logs)
    if not console_logs:
        pass
    else:
        global logs
        logs = logs + console_logs
    return console_logs


def get_end_time():
    global start_time
    end_time = time.time()
    test_duration = end_time - start_time
    if test_duration >= 60:
        minutes = round(test_duration / 60)
        seconds = test_duration % 60
        duration_str = f"{minutes} min {seconds} sec"
    else:
        seconds = round(test_duration)
        duration_str = f"{seconds} sec"
    return duration_str


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://localhost:7456/")

canvas = driver.find_element(By.ID, "GameCanvas")
time.sleep(3)

# Start Test

start_timestamp = dt.datetime.now()
start_time = time.time()
pyautogui.click(500, 500)
time.sleep(2)

checking = True
test_too_long = False

normal_interval = 0.9
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
                test_cases["TestCase_1"] = pass_text
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
                test_cases["TestCase_2"] = pass_text
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
                test_cases["TestCase_3"] = pass_text

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
                test_cases["TestCase_4"] = pass_text

    if time.time() > start_time + 20:
        checking = False
        driver.execute_script(f"console.log('Bird is NOT hitting any pipe for too long. Something is wrong!')")
        test_too_long = True

if not test_too_long:
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
                test_cases["TestCase_5"] = pass_text

if not test_too_long:
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
                        test_cases["TestCase_6"] = pass_text
                        checking = False

# TODO: 1. Screenshot 2. Get all logs from start to end. 3. Send report
time.sleep(2)  # Wait for Game Over
get_console_logs()  # final logs
driver.get_screenshot_as_file("game_over.png")
time.sleep(1)  # Enough time to render the screenshot.

test_report.bird_test_report(start_time=start_timestamp, duration=get_end_time(), logs=logs, testcases=test_cases)
