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
    str_list[4] = str_list[4].replace("[TIME]", now.strftime("%d/%m/%Y %H:%M:%S"))
    content = "".join(str_list)
    content = MIMEText(content, "html")
    report_email.attach(content)

    img_file = open("result.png", "rb")
    screenshot = MIMEImage(img_file.read())
    img_file.close()

    screenshot.add_header('Content-ID', '<result_screenshot>')
    report_email.attach(screenshot)

    # time.sleep(5)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()  # Secures the connection
        connection.login(user=MY_EMAIL, password=GMAIL_APP_PWD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg=report_email.as_string())


# write_report("Screenshot as Email")