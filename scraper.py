import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup
from mimetypes import guess_extension


driver_path = "/home/samaygandhi/Documents/chromedriver"
    
options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/brave-browser"
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)

driver.get("https://ceoelection.maharashtra.gov.in/searchlist/")

# district = sys.argv[1]
# assemblyConstituency = sys.argv[2]
# part = sys.argv[3]

district = "Mumbai City"
assemblyConstituency = "181 - Mahim"
part = 105

print(driver.find_element(By.ID, "ctl00_Content_DistrictList"))

selectDistrict = Select(driver.find_element(By.ID,"ctl00_Content_DistrictList"))

print(selectDistrict)

selectDistrict.select_by_visible_text(district)

selectAssemblyConstituency = Select(driver.find_element(By.ID, "ctl00_Content_AssemblyList"))

selectAssemblyConstituency.select_by_visible_text(assemblyConstituency)

selectPart = Select(driver.find_element(By.ID, "ctl00_Content_PartList"))

selectPart.select_by_value(str(part))

s = requests.session()
# s.headers.update(headers)


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
