from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# TODO
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from mimetypes import guess_extension
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
from ..mainCaptcha import main
from ..scraperResponse import ScraperResponse
# from .captcha import main


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

        district = district if district else "Mumbai City"
        assemblyConstituency = assemblyConstituency if assemblyConstituency else "181 - Mahim"
        part = pollingPart if pollingPart else "105"

        selectDistrict = Select(self.DRIVER.find_element(By.ID,"ctl00_Content_DistrictList"))
        selectDistrict.select_by_visible_text(district)

        selectAssemblyConstituency = Select(self.DRIVER.find_element(By.ID, "ctl00_Content_AssemblyList"))
        selectAssemblyConstituency.select_by_visible_text(assemblyConstituency)

        selectPart = Select(self.DRIVER.find_element(By.ID, "ctl00_Content_PartList"))
        selectPart.select_by_value(str(part))

        s = requests.session()

        r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/")

        for cookie in self.DRIVER.get_cookies():
            c = {cookie['name']: cookie['value']}
            s.cookies.update(c)


        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/Captcha.aspx")
            if r.status_code == 200:
                guess = guess_extension(r.headers['content-type'])
                if not guess: guess = ".png"
                captcha_file_path = "scripts/maharashtra/captcha" + guess
                self.SCRAPER_RESPONSE.captcha_generated = Path(captcha_file_path)
                if guess:
                    with open(captcha_file_path, "wb") as f:
                        f.write(r.content)
                    # Image.open(BytesIO(r.content)).show()
            else:
                self.SCRAPER_RESPONSE.message += "\n Could not solve Captcha."
                return self.SCRAPER_RESPONSE

        CAPTCHA_TEXT = main("maharashtra")
        print(f"Captcha Text obtained: {CAPTCHA_TEXT}")

        self.DRIVER.find_element(By.ID, "ctl00_Content_txtcaptcha").send_keys(CAPTCHA_TEXT)
        self.DRIVER.find_element(By.ID, "ctl00_Content_OpenButton").click()


        # r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/ViewPDF.aspx")

        print("Parsing PDF...")
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/ViewPDF.aspx")
            if r.status_code == 200:
                guess = guess_extension(r.headers['content-type'])
                if not guess: guess = ".pdf"
                pdf_file_path = "scripts/maharashtra/electoral_rolls" + guess
                self.SCRAPER_RESPONSE.electoral_roll_PDF = Path(pdf_file_path)
                if guess:
                    print("Storing pdf...")
                    with open(pdf_file_path, "wb") as f:
                        f.write(r.content)
                    self.SCRAPER_RESPONSE.status = True
            else:
                self.SCRAPER_RESPONSE.message = "Could not store Electoral PDFs"

        return self.SCRAPER_RESPONSE
 
