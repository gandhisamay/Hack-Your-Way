from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import requests
from ..mainCaptcha import Captcha_To_Txt, main
from ..scraperResponse import VoterPortalResponse 
from time import sleep

class DetailedData:
    def __init__(self, name, age, father_or_husband_name, gender, state, district, assembly_constituency):
        self.name = name
        self.age = age
        self.father_or_husband_name = father_or_husband_name
        self.gender = gender
        self.state = state
        self.district = district
        self.assembly_constituency = assembly_constituency

class EpicData:
    def __init__(self, epic_no, state):
        self.epic_no = epic_no
        self.state = state


class VoterPortalScraper:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        options.add_argument('--headless=chrome')
        options.add_argument('--disable-dev-shm-usage')

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
            guess = ".png"
            with open("scripts/voter_portal/captcha" + guess, "wb") as f:
                f.write(r.content)

        CAPTCHA_TEXT = main("voter_portal")
        return CAPTCHA_TEXT

    def extract_results(self):
        # try:
        self.SCRAPER_RESPONSE = VoterPortalResponse() 
        self.SCRAPER_RESPONSE.epic_no = self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='epic_no_plain']").get_attribute('value')
        self.SCRAPER_RESPONSE.name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='name']").get_attribute('value')
        self.SCRAPER_RESPONSE.gender=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='gender']").get_attribute('value')
        self.SCRAPER_RESPONSE.age=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='age']").get_attribute('value')
        self.SCRAPER_RESPONSE.father_or_husband_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='rln_name']").get_attribute('value')
        self.SCRAPER_RESPONSE.state=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='state']").get_attribute('value')
        self.SCRAPER_RESPONSE.district=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='district']").get_attribute('value')
        self.SCRAPER_RESPONSE.assembly_constituency_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='ac_name']").get_attribute('value')
        self.SCRAPER_RESPONSE.assembly_constituency_no=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='ac_no']").get_attribute('value')
        self.SCRAPER_RESPONSE.parliamentary_constituency_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='pc_name']").get_attribute('value')
        self.SCRAPER_RESPONSE.part_number=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='part_no']").get_attribute('value')
        self.SCRAPER_RESPONSE.polling_station_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='ps_name']").get_attribute('value')
        print(self.SCRAPER_RESPONSE)
        # except:
            # print("Failed to get response, the voter information portal is slow. Please try again")

    def epic_search(self, epicData: EpicData):
        url = "https://electoralsearch.in"
        self.DRIVER.get(url)
        sleep(1)

        self.DRIVER.find_element(By.ID, 'continue').click()
        sleep(1)

        tab1=self.DRIVER.find_element(By.CSS_SELECTOR, "li[role='tab']")
        self.DRIVER.execute_script("arguments[0].setAttribute('class','')", tab1)
        self.DRIVER.execute_script("arguments[0].setAttribute('role','')", tab1)

        tab2=self.DRIVER.find_element(By.CSS_SELECTOR, "li[role='tab']")
        self.DRIVER.execute_script("arguments[0].setAttribute('class','active')", tab2)
        tab2.click()

        self.DRIVER.find_element(By.ID, "name").send_keys(epicData.epic_no)
        Select(self.DRIVER.find_element(By.ID, "epicStateList")).select_by_visible_text(epicData.state)

        captcha = self.get_session_captcha() 
        self.DRIVER.find_element(By.ID, "txtEpicCaptcha").send_keys(captcha)

        self.DRIVER.execute_script("document.querySelector('#btnEpicSubmit').click()")
        sleep(40)

        forms = self.DRIVER.find_elements(By.TAG_NAME, "form")
        print(forms)

        self.extract_results()

    def detailed_search(self, detailedData: DetailedData):
        url = "https://electoralsearch.in"
        self.DRIVER.get(url)
        sleep(1)

        self.DRIVER.find_element(By.ID, 'continue').click()

        self.DRIVER.find_element(By.NAME, "name").send_keys(detailedData.name)
        self.DRIVER.find_element(By.ID, "txtFName").send_keys(detailedData.father_or_husband_name)

        Select(self.DRIVER.find_element(By.ID, "listGender")).select_by_value(detailedData.gender)
        Select(self.DRIVER.find_element(By.ID, "nameStateList")).select_by_visible_text(detailedData.state)
        sleep(1)

        drop_down_boxes = self.DRIVER.find_elements(By.ID, "namelocationList")
        district_drop_down =  drop_down_boxes[0]
        assembly_constituency_drop_down = drop_down_boxes[1]
        Select(district_drop_down).select_by_visible_text(detailedData.district)
        sleep(1)
        Select(assembly_constituency_drop_down).select_by_visible_text(detailedData.assembly_constituency)

        Select(self.DRIVER.find_element(By.ID, "ageList")).select_by_visible_text(detailedData.age)

        captcha = self.get_session_captcha()
        self.DRIVER.find_element(By.ID, "txtCaptcha").send_keys(captcha)

        self.DRIVER.execute_script("document.querySelector('#btnDetailsSubmit').click()")

        sleep(50)
        forms = self.DRIVER.find_elements(By.TAG_NAME, "form")
        print(forms)

        self.extract_results()
        
 
detailed_data = DetailedData(name="Nirali Gandhi", father_or_husband_name="Amit Gandhi", age="45", state="Maharashtra", district="Mumbai Suburban", assembly_constituency="Borivali", gender="F")
epic_data = EpicData(epic_no="YBB4915526", state="Maharashtra")
scraper = VoterPortalScraper()
# scraper.detailed_search(detailedData=detailedData)
scraper.epic_search(epic_data)
