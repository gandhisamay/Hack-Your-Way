from platform import version
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# TODO
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import os
import requests
from bs4 import BeautifulSoup
from mimetypes import guess_extension
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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

    def run(self, district, assemblyConstituency, pollingPart):
        s = requests.session()
        assemblyCode = assemblyConstituency if assemblyConstituency else 6
        partNumber = pollingPart if pollingPart else 30
        url = f"https://ceogoa.nic.in/PDF/EROLL/MOTHERROLL/2021/{assemblyCode}/S05A{assemblyCode}P{partNumber}.pdf"
        r = s.get(url, verify=False)
        if r.status_code == 200:
            guess = guess_extension(r.headers['content-type'])
            if not guess: guess = ".pdf"
            if guess:
                print("Storing pdf...")
                with open("scripts/goa/electoral_rolls" + guess, "wb") as f:
                    f.write(r.content)
         
