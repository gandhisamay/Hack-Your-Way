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
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

s = requests.session()

assemblyCode = 3
partNumber = 1
assemblyCodeString ="3-MAMIT"
url = f"https://ceo.mizoram.gov.in/ERollReportWithoutPhoto/S16/{assemblyCodeString}/S16A{assemblyCode}P{partNumber}.pdf"
# https://ceo.mizoram.gov.in/ERollReportWithoutPhoto/S16/3-MAMIT/S16A3P1.pdf

r = s.get(url)
print(r.status_code)
if r.status_code == 200:
    guess = guess_extension(r.headers['content-type'])
    if not guess: guess = ".pdf"
    if guess:
        print("Storing pdf...")
        with open("electoral_rolls" + guess, "wb") as f:
            f.write(r.content)
 
