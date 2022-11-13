from chromedriver_autoinstaller.utils import download_chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
# TODO
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import requests
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from mimetypes import guess_extension
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
from time import sleep
from ..scraperResponse import ScraperResponse
# from captcha import main


# driver_path = "/home/samaygandhi/Documents/chromedriver"
# options.binary_location = "/usr/bin/brave-browser"
    
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
        self.SCRAPER_RESPONSE.captcha_generated = None
        # driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
        # driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=options)

    def run(self, district, assemblyConstituency, pollingPart):
        self.DRIVER.get("https://erms.gujarat.gov.in/ceo-gujarat/master/frmEPDFRoll.aspx")
        self.DRIVER.maximize_window()
        # district = "3-Patan"
        # assembly = "16-Radhanpur"
        assemblyCode = assemblyConstituency if assemblyConstituency else 141
        partNumber = pollingPart if pollingPart else 22
        # pollingArea = "Samavas, Eval,Anusuchit Jati Vas Eval,Rabari Vas, Eval,Kolivas, Eval"
        s = requests.session()
        url = f"https://erms.gujarat.gov.in/ceo-gujarat/DRAFT2022/{assemblyCode}/S06A{assemblyCode}P{partNumber}.pdf"
        r = s.get(url)
        if r.status_code == 200:
            guess = guess_extension(r.headers['content-type'])
            if not guess: guess = ".pdf"
            pdf_file_path = "scripts/gujarat/electoral_rolls" + guess
            self.SCRAPER_RESPONSE.electoral_roll_PDF = Path(pdf_file_path)
            if guess:
                print("Storing pdf...")
                with open(pdf_file_path, "wb") as f:
                    f.write(r.content)
                print("PDF written.")
                self.SCRAPER_RESPONSE.status = True
        else:
            self.SCRAPER_RESPONSE.message = "Could not store Electoral PDFs"

        return self.SCRAPER_RESPONSE

if __name__ == "__main__":
    scraper_class = ScraperClass()
    scraper_class.run(None, None, None)
