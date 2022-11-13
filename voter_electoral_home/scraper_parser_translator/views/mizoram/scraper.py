from platform import version
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# TODO
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import os
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from mimetypes import guess_extension
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ..scraperResponse import ScraperResponse
import chromedriver_autoinstaller
# from ..mainCaptcha import main
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
        self.SCRAPER_RESPONSE.captcha_generated = None

    def run(self, district, assemblyConstituency, pollingPart):
        s = requests.session()

        partNumber = pollingPart if pollingPart else 1
        assemblyCodeString = assemblyConstituency if assemblyConstituency else "3-MAMIT"
        ############ TODO!!!!!!!!!!!! MIZORAM Code 
        assemblyCode = assemblyConstituency if assemblyConstituency else 3
        url = f"https://ceo.mizoram.gov.in/ERollReportWithoutPhoto/S16/{assemblyCodeString}/S16A{assemblyCode}P{partNumber}.pdf"
# https://ceo.mizoram.gov.in/ERollReportWithoutPhoto/S16/3-MAMIT/S16A3P1.pdf

        r = s.get(url)
        print(r.status_code)
        if r.status_code == 200:
            guess = guess_extension(r.headers['content-type'])
            if not guess: guess = ".pdf"
            pdf_file_path = "scripts/mizoram/electoral_rolls" + guess
            self.SCRAPER_RESPONSE.electoral_roll_PDF = Path(pdf_file_path)
            if guess:
                print("Storing pdf...")
                with open(pdf_file_path, "wb") as f:
                    f.write(r.content)
                self.SCRAPER_RESPONSE.status = True
        else:
            self.SCRAPER_RESPONSE.message = "Could not store Electoral PDFs"

        return self.SCRAPER_RESPONSE
         
