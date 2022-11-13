from selenium import webdriver
from selenium.webdriver.common.by import By
# TODO
# from selenium.self.DRIVER.support.ui import Select
from selenium.webdriver.support.select import Select
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ..mainCaptcha import main
from time import sleep

class Voter:
    def __init__(self, name, age, father_or_husband_name, gender, state, district, assembly_constituency):
        self.name = name
        self.age = age
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

    def run2(self, voter):
        url = "https://electoralsearch.in"
        self.DRIVER.get(url)

        captcha = self.get_session_captcha()

        # for cookie in self.DRIVER.get_cookies():
        #     c = {cookie['name']: cookie['value']}
        #     self.SESSION.cookies.update(c)
        #
        payload = {
        "age": 20,
        "dob": "1976-12-17",
        "gender": "F",
        "location": "S13,,",
        "location_range": "20",
        "name": "Nirali Amit Gandhi",
        "page_no": 1,
        "results_per_page": 10,
        "reureureired": "ca3ac2c8-4676-48eb-9129-4cdce3adf6ea",
        "rln_name": "Amit Gandhi",
        "search_type": "details",
        "txtCaptcha": captcha,
        }

        response = requests.post("https://electoralsearch.in/Home/searchVoter", payload)
        print(response.content)
        print(response.text)
        print(response.json)


    def run(self, voter):
        url = "https://electoralsearch.in"
        self.DRIVER.get(url)
        # print(BeautifulSoup(self.DRIVER.page_source, 'lxml').prettify)
        sleep(2)
        self.DRIVER.find_element(By.NAME, "name").send_keys(voter.name)
        self.DRIVER.find_element(By.ID, "txtFName").send_keys(voter.father_or_husband_name)

        Select(self.DRIVER.find_element(By.ID, "listGender")).select_by_value(voter.gender)
        # TODO check later whether to do this by value of name of the state.
        Select(self.DRIVER.find_element(By.ID, "nameStateList")).select_by_visible_text(voter.state)
        sleep(1)
        drop_down_boxes = self.DRIVER.find_elements(By.ID, "namelocationList")
        district_drop_down =  drop_down_boxes[0]
        assembly_constituency_drop_down = drop_down_boxes[1]
        selectDistrict = Select(district_drop_down)
        selectDistrict.select_by_visible_text(voter.district)
        sleep(1)
        selectConstitutency = Select(assembly_constituency_drop_down)
        selectConstitutency.select_by_visible_text(voter.assembly_constituency)

        # for option in selectConstitutency.options:
        #     print(option.text)

        # print(selectDistrict.options)
        # print(selectConstitutency.options)
        # for option in selectConstitutency.options:
            # print(option.text)
        # Select(district_drop_down).select_by_visible_text(voter.district)
        # Select(assembly_constituency_drop_down).select_by_visible_text(voter.assembly_constituency)

        #Age related stuff 
        # self.DRIVER.find_element(By.CSS_SELECTOR, "input#radDob").click()
        # self.DRIVER.find_element(By.ID, "radDob").click()
        Select(self.DRIVER.find_element(By.ID, "ageList")).select_by_visible_text(voter.age)
        captcha = self.get_session_captcha()

        self.DRIVER.find_element(By.ID, "txtCaptcha").send_keys(captcha)

        # button = self.DRIVER.find_element(By.TAG_NAME, "button")
        # button.click()
        # self.DRIVER.find_element(By.ID, "btnDetailsSubmit").click()
        self.DRIVER.execute_script("document.querySelector('#btnDetailsSubmit').click()")

        sleep(40)
        
        forms = self.DRIVER.find_elements(By.TAG_NAME, "form")

        print(forms)
        # print(len(forms))
        # if len(forms) <= 2:
        #     print("Please try again error getting results from electoral rolls")
        # else:
        #     form = forms[2]
        #     epic_id = form.find_element(By.NAME, "epic_no_plain").text
        #     print(epic_id)
        #
        details=[]
        c_id=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='id']").get_attribute('value')
        epic_no=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='epic_no_plain']").get_attribute('value')
        name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='name']").get_attribute('value')
        gender=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='gender']").get_attribute('value')
        age=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='age']").get_attribute('value')
        rln_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='rln_name']").get_attribute('value')
        last_update=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='last_update']").get_attribute('value')
        state=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='state']").get_attribute('value')
        district=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='district']").get_attribute('value')
        ac_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='ac_name']").get_attribute('value')
        ac_no=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='ac_no']").get_attribute('value')
        pc_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='pc_name']").get_attribute('value')
        ps_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='ps_name']").get_attribute('value')
        slno_inpart=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='slno_inpart']").get_attribute('value')
        st_code=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='st_code']").get_attribute('value')
        ps_lat_long=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='ps_lat_long']").get_attribute('value')
        part_no=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='part_no']").get_attribute('value')
        part_name=self.DRIVER.find_element(By.CSS_SELECTOR, "input[name='part_name']").get_attribute('value')

        details.append((c_id,epic_no,name,gender,age,rln_name,last_update,state,district,ac_name,ac_no,pc_name,ps_name,slno_inpart,st_code,ps_lat_long,part_no,part_name))

        print(details)
        

voter = Voter(name="Nirali Gandhi", father_or_husband_name="Amit Gandhi", age="45", state="Maharashtra", district="Mumbai Suburban", assembly_constituency="Borivali", gender="F")
scraper = ScraperClass()
scraper.run(voter=voter)
