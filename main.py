import time, smtplib, ssl, os

from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Email:
    load_dotenv()

    def __init__(self):
        self.my_email = os.getenv("MY_EMAILS")
        self.password = os.getenv("PASSWORDS")
        self.mottagare = os.getenv("MOTTAGARES")
        self.smtp_server = "smtp.gmail.com"
        self.port = 587

    def message_email(self):
        message = MIMEMultipart("mixed")
        message["From"] = self.my_email
        message["To"] = ", ".join(self.mottagare)
        message["Subject"] = "Polisen: Det finns en ledig tid"
        msg_content = "<h4>Morsningkorsning,<br> Det finns en ledig tid att boka nu hörru!<br> <br> Med supervänliga hälsningar,<br> Petter-Niklas Gyllenstånd</h4>\n"
        body = MIMEText(msg_content, "html")
        message.attach(body)

        file_url = "lediga_tider.png"
        try:
            with open(file_url, "rb") as f:
                p = MIMEApplication(f.read(), _subtype="png")
                p.add_header(
                    "Content-Disposition",
                    "attachment; filename= %s" % file_url.split("\\")[-1],
                )
                message.attach(p)
        except Exception as e:
            print(e)
        finally:
            self.msg_full = message.as_string()
            return self.msg_full

    def send_email(self):

        self.message_email()

        context = ssl.create_default_context()

        try:
            connection = smtplib.SMTP(self.smtp_server, self.port)
            connection.ehlo()
            connection.starttls(context=context)
            connection.ehlo()
            connection.login(self.my_email, self.password)
            connection.ehlo()
            connection.sendmail(
                self.my_email,
                self.mottagare,
                self.msg_full,
            )
        except Exception as e:
            print(e)
        finally:
            connection.quit()


class Browser:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("user-data-dir=C:\PythonProjects\Selenium")
        self.options.add_argument("--log-level-3")
        self.options.add_argument("--headless")
        self.options.add_argument("--ignore-certificate-errors-spki-list")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--ignore-ssl-errors")
        self.s = Service("C:\PythonProjects\chromedriver.exe")  # Your webdriver

        self.URL = (
            "https://bokapass.nemoq.se/Booking/Booking/Index/ditt_lan"  # Your region
        )

    def xpath_name(self, xpath):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()

    def lediga_tider(self):
        self.driver = webdriver.Chrome(service=self.s, options=self.options)
        self.driver.get(self.URL)

        self.xpath_name('//*[@name="StartNextButton"]')
        self.xpath_name('//*[@name="AcceptInformationStorage"]')
        self.xpath_name('//*[@name="Next"]')
        self.xpath_name('//*[@name="ServiceCategoryCustomers[0].ServiceCategoryId"]')
        self.xpath_name('//*[@name="Next"]')
        self.xpath_name('//*[@name="SectionId"]')
        self.xpath_name('//*[@value="00"]')  # Value of town
        self.xpath_name('//*[@name="TimeSearchFirstAvailableButton"]')

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div/div/form[2]/div[2]/table/thead/tr",
                )
            )
        )
        datum = self.driver.find_elements(
            By.XPATH, "/html/body/div[2]/div/div/div/form[2]/div[2]/table/thead/tr"
        )

        for date in datum:
            if "mar" in date.text or "apr" in date.text:
                print("Det finns en ledig tid")

                lediga_tider_shot = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@class="timetable"]')
                    )
                )
                lediga_tider_shot.screenshot("lediga_tider.png")

                emails = Email()
                emails.send_email()

                self.driver.close()
                ingen_ledig_tid = False

                return ingen_ledig_tid

            else:
                print("Ingen ledig tid")

                self.driver.close()
                time.sleep(600)  # Godnatt


ingen_ledig_tid = True

while ingen_ledig_tid:
    browser = Browser()
    browser.lediga_tider()
