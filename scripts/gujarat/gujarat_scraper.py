from chromedriver_autoinstaller.utils import download_chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
# TODO
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import requests

from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from mimetypes import guess_extension
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
from time import sleep
# from captcha import main


driver_path = "/home/samaygandhi/Documents/chromedriver"
    
options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/brave-browser"
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--incognito')
options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
# driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=options)
driver.get("https://erms.gujarat.gov.in/ceo-gujarat/master/frmEPDFRoll.aspx")
driver.maximize_window()

district = "3-Patan"
assembly = "16-Radhanpur"
assemblyCode = 141
partNumber = 22
pollingArea = "Samavas, Eval,Anusuchit Jati Vas Eval,Rabari Vas, Eval,Kolivas, Eval"

s = requests.session()

url = f"https://erms.gujarat.gov.in/ceo-gujarat/DRAFT2022/{assemblyCode}/S06A{assemblyCode}P{partNumber}.pdf"

r = s.get(url)
if r.status_code == 200:
    guess = guess_extension(r.headers['content-type'])
    if not guess: guess = ".png"
    if guess:
        with open("captcha" + guess, "wb") as f:
            f.write(r.content)
