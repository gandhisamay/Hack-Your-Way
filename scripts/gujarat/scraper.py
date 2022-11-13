from selenium import webdriver
import requests
from pathlib import Path
from mimetypes import guess_extension
from ..scraperResponse import ScraperResponse

# driver_path = "/home/samaygandhi/Documents/chromedriver"
# options.binary_location = "/usr/bin/brave-browser"
    
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
        # driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
        # driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=options)

    def run(self, district, assemblyConstituency, pollingPart):
        self.DRIVER.get("https://erms.gujarat.gov.in/ceo-gujarat/master/frmEPDFRoll.aspx")
        self.DRIVER.maximize_window()
        # district = "3-Patan"
        # assembly = "16-Radhanpur"
        assemblyCode = assemblyConstituency.split('-')[1].strip()
        partNumber = pollingPart
        assemblyCodeDir = assemblyCode

        if len(assemblyCode)==1:
            assemblyCodeDir = f"00{assemblyCode}"
        elif len(assemblyCode)==2:
            assemblyCodeDir = f"0{assemblyCode}"

        s = requests.session()
        url = f"https://erms.gujarat.gov.in/ceo-gujarat/DRAFT2022/{assemblyCodeDir}/S06A{assemblyCode}P{partNumber}.pdf"
        r = s.get(url)
        if r.status_code == 200:
            guess = guess_extension(r.headers['content-type'])
            if not guess: guess = ".pdf"
            pdf_file_path = "scripts/gujarat/electoral_rolls" + guess
            self.SCRAPER_RESPONSE.electoral_roll_PDF = Path(pdf_file_path)
            if guess:
                print("Storing pdf...")
                with open(pdf_file_path, "wb") as f:
                    f.write(r.content)
                print("PDF written.")
                self.SCRAPER_RESPONSE.status = True
        else:
            self.SCRAPER_RESPONSE.message = "Could not store Electoral PDFs"

        return self.SCRAPER_RESPONSE

if __name__ == "__main__":
    scraper_class = ScraperClass()
    scraper_class.run(None, None, None)
