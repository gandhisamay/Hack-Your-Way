import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

print(driver.find_element(By.ID, "ctl00_Content_DistrictList"))

selectDistrict = Select(driver.find_element(By.ID,"ctl00_Content_DistrictList"))

print(selectDistrict)

selectDistrict.select_by_visible_text(district)

selectAssemblyConstituency = Select(driver.find_element(By.ID, "ctl00_Content_AssemblyList"))

selectAssemblyConstituency.select_by_visible_text(assemblyConstituency)

selectPart = Select(driver.find_element(By.ID, "ctl00_Content_DistrictList"))

selectPart.select_by_visible_text("2 - K.A.Subramaniam Road, Matunga, Mumbai-19")

# soup = BeautifulSoup(driver.page_source, 'lxml')

# print(driver.page_source)

# print(soup)

