from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import os
from time import sleep
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from mimetypes import guess_extension
from ..mainCaptcha import main
from ..scraperResponse import ScraperResponse


# driver_path = "/home/samaygandhi/Documents/chromedriver"
# chromedriver_autoinstaller.install()
    
class ScraperClass:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.DRIVER = webdriver.Chrome(options=options)
        self.SCRAPER_RESPONSE = ScraperResponse()
        # driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
        # driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=options)

    def run(self, district, assemblyConstituency, pollingPart):
        self.DRIVER.get("https://ceoelection.maharashtra.gov.in/searchlist/")

        sleep(1)
        selectDistrict = Select(self.DRIVER.find_element(By.ID,"ctl00_Content_DistrictList"))
        selectDistrict.select_by_visible_text(district)

        sleep(1)
        
        rev = str(reversed(assemblyConstituency))
        left = rev.split("-", 1)[0]
        right = rev.split("-", 1)[1]
        assemblyConstituency = left + " - " + right
        # AS_name = str(assemblyConstituency.rsplit("-", 1)[0])
        selectAssemblyConstituency = Select(self.DRIVER.find_element(By.ID, "ctl00_Content_AssemblyList"))
        selectAssemblyConstituency.select_by_visible_text(assemblyConstituency)

        sleep(1)
        selectPart = Select(self.DRIVER.find_element(By.ID, "ctl00_Content_PartList"))
        selectPart.select_by_value(str(pollingPart))

        s = requests.session()

        r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/")

        for cookie in self.DRIVER.get_cookies():
            c = {cookie['name']: cookie['value']}
            s.cookies.update(c)


        if r.status_code == 200:
            r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/Captcha.aspx")
            if r.status_code == 200:
                guess = guess_extension(r.headers['content-type'])
                if not guess: guess = ".png"
                captcha_file_path = "/scraper_parser_translator/views/maharashtra/captcha" + guess
                captcha_file_path = (os.path.abspath(os.getcwd()) + captcha_file_path)
                print(captcha_file_path)
                self.SCRAPER_RESPONSE.captcha_generated = (captcha_file_path)
                if guess:
                    with open(captcha_file_path, "wb") as f:
                        f.write(r.content)

            else:
                self.SCRAPER_RESPONSE.message += "\n Could not solve Captcha."
                return self.SCRAPER_RESPONSE

        CAPTCHA_TEXT = main("maharashtra")
        print(f"Captcha Text obtained: {CAPTCHA_TEXT}")

        self.DRIVER.find_element(By.ID, "ctl00_Content_txtcaptcha").send_keys(CAPTCHA_TEXT)
        self.DRIVER.find_element(By.ID, "ctl00_Content_OpenButton").click()

        print("Parsing PDF...")
        if r.status_code == 200:
            r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/ViewPDF.aspx")
            if r.status_code == 200:
                guess = guess_extension(r.headers['content-type'])
                if not guess: guess = ".pdf"
                pdf_file_path = "/scraper_parser_translator/views/maharashtra/electoral_rolls" + guess
                pdf_file_path = (os.path.abspath(os.getcwd()) + pdf_file_path)
                print(pdf_file_path)
                self.SCRAPER_RESPONSE.electoral_roll_PDF = pdf_file_path
                if guess:
                    print("Storing pdf...")
                    with open(pdf_file_path, "wb") as f:
                        f.write(r.content)
                    self.SCRAPER_RESPONSE.status = True
            else:
                self.SCRAPER_RESPONSE.message = "Could not store Electoral PDFs"

        return self.SCRAPER_RESPONSE
 

