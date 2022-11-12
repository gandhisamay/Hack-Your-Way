from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# TODO
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import requests
from bs4 import BeautifulSoup
from mimetypes import guess_extension
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
from captcha import main


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
# driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
# driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=options)

driver.get("https://ceoelection.maharashtra.gov.in/searchlist/")

district = "Mumbai City"
assemblyConstituency = "181 - Mahim"
part = 105

selectDistrict = Select(driver.find_element(By.ID,"ctl00_Content_DistrictList"))
selectDistrict.select_by_visible_text(district)

selectAssemblyConstituency = Select(driver.find_element(By.ID, "ctl00_Content_AssemblyList"))
selectAssemblyConstituency.select_by_visible_text(assemblyConstituency)

selectPart = Select(driver.find_element(By.ID, "ctl00_Content_PartList"))
selectPart.select_by_value(str(part))

s = requests.session()

r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/")

for cookie in driver.get_cookies():
    c = {cookie['name']: cookie['value']}
    s.cookies.update(c)


if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/Captcha.aspx")
    if r.status_code == 200:
        guess = guess_extension(r.headers['content-type'])
        if not guess: guess = ".png"
        if guess:
            with open("captcha" + guess, "wb") as f:
                f.write(r.content)
            # Image.open(BytesIO(r.content)).show()

CAPTCHA_TEXT = main()
print(f"Captcha Text obtained: {CAPTCHA_TEXT}")

driver.find_element(By.ID, "ctl00_Content_txtcaptcha").send_keys(CAPTCHA_TEXT)
driver.find_element(By.ID, "ctl00_Content_OpenButton").click()


# r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/ViewPDF.aspx")

print("Parsing PDF...")
if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    r = s.get("https://ceoelection.maharashtra.gov.in/searchlist/ViewPDF.aspx")
    if r.status_code == 200:
        guess = guess_extension(r.headers['content-type'])
        if not guess: guess = ".pdf"
        if guess:
            print("Storing pdf...")
            with open("electoral_rolls" + guess, "wb") as f:
                f.write(r.content)
 
