import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import datetime as dt
import time

MY_EMAIL = "muhsen.10ktech@gmail.com"
GMAIL_APP_PWD = "kxwlcunxqitnoaap"

now = dt.datetime.now()

report_email = MIMEMultipart("alternative")
report_email["Subject"] = f"QA Automated Test Completed"
report_email["From"] = MY_EMAIL
report_email["To"] = MY_EMAIL


def write_report(test_name):
    template_filepath = f"./qareport.html"

    with open(template_filepath, encoding='utf-8') as report_template:
        str_list = report_template.readlines()

    str_list[3] = str_list[3].replace("[TESTNAME]", test_name)
    str_list[4] = str_list[4].replace("[TIME]", now.strftime("%H:%M:%S %d/%m/%Y"))
    content = "".join(str_list)
    content = MIMEText(content, "html")
    report_email.attach(content)

    img_file = open("result.png", "rb")
    screenshot = MIMEImage(img_file.read())
    img_file.close()

    screenshot.add_header('Content-ID', '<result_screenshot>')
    report_email.attach(screenshot)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()  # Secures the connection
        connection.login(user=MY_EMAIL, password=GMAIL_APP_PWD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg=report_email.as_string())


def display_logs(logs):
    all_logs_str = ""
    for i in logs:
        i.strip('\"')  # <- STILL DOES NOT WORK!
        all_logs_str = all_logs_str + i + "<br />"
    return all_logs_str


def bird_test_report(start_time, duration, logs, testcases):
    template_filepath = f"./smoketestreport.html"

    with open(template_filepath, encoding='utf-8') as report_template:
        str_list = report_template.readlines()

    str_list[4] = str_list[4].replace("[TIME]", start_time.strftime("%d/%m/%Y %H:%M:%S"))
    str_list[5] = str_list[5].replace("[DURATION]", duration)

    # -- DOES NOT WORK! --
    # for ls in str_list:
    #     if ls.find("TIME") != -1:
    #         ls.replace("[TIME]", start_time)
    #     elif ls.find("DURATION") != -1:
    #         ls.replace("[DURATION]", duration)

    html_line = 13
    for i in range(1, 7):
        str_list[html_line] = str_list[html_line].replace(f"[RESULT{i}]", testcases[f"TestCase_{i}"])
        if testcases[f"TestCase_{i}"].find("PASS") != -1:
            str_list[html_line] = str_list[html_line].replace("color:red", "color:green")
        html_line += 4

    str_list[47] = str_list[47].replace("[C_LOGS]", display_logs(logs))

    content = "".join(str_list)
    content = MIMEText(content, "html")
    report_email.attach(content)

    img_file = open("game_over.png", "rb")
    screenshot = MIMEImage(img_file.read())
    img_file.close()

    screenshot.add_header('Content-ID', '<game_over_screenshot>')
    report_email.attach(screenshot)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()  # Secures the connection
        connection.login(user=MY_EMAIL, password=GMAIL_APP_PWD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg=report_email.as_string())


