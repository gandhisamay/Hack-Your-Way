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

from ..mainCaptcha import main

class DateOfBirth:
    def __init__(self, day, month, year) -> None:
        self.day =day
        self.month = month 
        self.year = year

class Voter:
    def __init__(self, name, date_of_birth, father_or_husband_name, gender, state, district, assembly_constituency):
        self.name = name
        self.date_of_birth = date_of_birth
        self.father_or_husband_name = father_or_husband_name
        self.gender = gender
        self.state = state
        self.district = district
        self.assembly_constituency = assembly_constituency

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

        s = requests.session()
        self.SESSION = s

# /Home/GetCaptcha?image=true&id=Sun Nov 13 2022 07:43:13 GMT+0530 (India Standard Time)"
    def get_session_captcha(self) ->str: 
        for cookie in self.DRIVER.get_cookies():
            c = {cookie['name']: cookie['value']}
            self.SESSION.cookies.update(c)

        r = self.SESSION.get("https://electoralsearch.in/Home/GetCaptcha?image=true")
        if r.status_code == 200:
            guess = guess_extension(r.headers['content-type'])
            if not guess: guess = ".png"
            if guess:
                with open("scripts/voter_portal/captcha" + guess, "wb") as f:
                    f.write(r.content)

        CAPTCHA_TEXT = main("voter_portal")
        return CAPTCHA_TEXT

    def run(self, voter):
        self.DRIVER.get("https://electoralsearch.in/")
        self.DRIVER.find_element(By.ID, "name1").send_keys(voter.name)
        self.DRIVER.find_element(By.ID, "txtFName").send_keys(voter.father_or_husband_name)

        Select(self.DRIVER.find_element(By.ID, "listGender")).select_by_value(voter.gender)
        # TODO check later whether to do this by value of name of the state.
        Select(self.DRIVER.find_element(By.ID, "nameStateList")).select_by_visible_text(voter.state)
        drop_down_boxes = self.DRIVER.find_elements(By.ID, "namelocationList")
        district_drop_down =  drop_down_boxes[0]
        assembly_constituency_drop_down = drop_down_boxes[1]
        Select(district_drop_down).select_by_visible_text(voter.district)
        Select(assembly_constituency_drop_down).select_by_visible_text(voter.assembly_constituency)

        #Age related stuff 
        self.DRIVER.find_element(By.ID, "radDob").click()
        Select(self.DRIVER.find_element(By.ID, "yearList")).select_by_visible_text(voter.date_of_birth.year)
        Select(self.DRIVER.find_element(By.ID, "monthList")).select_by_visible_text(voter.date_of_birth.monthList)
        Select(self.DRIVER.find_element(By.ID, "dayList")).select_by_visible_text(voter.date_of_birth.dayList)

        captcha = self.get_session_captcha()

        self.DRIVER.find_element(By.ID, "txtCaptcha").send_keys(captcha)
        self.DRIVER.find_element(By.ID, "btnDetailsSubmit").click()

        self.DRIVER.find_element(By.XPATH, "//form[@action='/Home/VoterInformation']").click()
        print(self.DRIVER.current_url)


dob = DateOfBirth(day="19", year="2001", month="Dec")
print(dob)
voter = Voter(name="Aditya Sheth", father_or_husband_name="Milap Sheth", date_of_birth=dob, state="Gujarat", district="Vadodara", assembly_constituency="Dabhoi", gender="M")

ScraperClass(voter).run()
