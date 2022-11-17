import os
import csv
import json
import subprocess
from .scraperResponse import ScraperResponse, UserInput
from .maharashtra.scraper import ScraperClass as MaharashtraScraper
from .gujarat.scraper import ScraperClass as GujuratScraper
from .goa.scraper import ScraperClass as GoaScraper
from .sikkim.scraper import ScraperClass as SikkimScraper
from .mizoram.scraper import ScraperClass as MizoramScraper
from .pdf_to_txt.pdf import PDF_to_Txt
from .txt_to_csv.multi_lang_processing import parse_english
from .voter_portal.scraper import VoterPortalScraper, EpicData, DetailedData
    

class MainScraper:
    def __init__(self) -> None:
        self.VOTER_PORTAL_SCRAPER = VoterPortalScraper()
        self.STATE_SCRAPER_MAP = {"Maharashtra": MaharashtraScraper,
            "Gujarat": GujuratScraper,
            "Goa": GoaScraper,
            "Sikkim": SikkimScraper,
            "Mizoram": MizoramScraper}
        self.STATE_LANGUAGE = {"Maharashtra": "mr",
            "Gujarat": "gu",
            "Goa": "en",
            "Sikkim": "en",
            "Mizoram": "en"}
        self.PDF_TO_TXT_PARSER = PDF_to_Txt()

    def callVoterPortal(self, epicSearch, UserInput):
        # GENDER - M/F/O, age - str
        try:
            response = None
            if epicSearch:
                data = EpicData(epic_no=UserInput.epic_no, state=UserInput.state)
                response = self.VOTER_PORTAL_SCRAPER.epic_search(data)
            else:
                # subprocess.call("npm list")
                # subprocess.run(["npm list"])
                data = DetailedData(name=UserInput.name, father_or_husband_name=UserInput.father_or_husband_name, 
                                    age=UserInput.age, state=UserInput.state, district=UserInput.district, 
                                    assembly_constituency=UserInput.assembly_constituency, gender=UserInput.gender)
                subprocess.run(["node", "scraper_parser_translator/views/voter_portal_js/index.js"])
                print(f"Data for detailed Search:\n {data}")
                # response = self.VOTER_PORTAL_SCRAPER.detailed_search(data)
            return response
        except Exception as e:
            print(e)
            return None
    # detailed_data = DetailedData(name="Aditya Sheth", father_or_husband_name="Milap Sheth", age="20", state="Gujarat", district="Vadodara", assembly_constituency="Dabhoi", gender="M")

    def callParticularScraper(self, state, district, assemblyConstituency, pollingPart):
        try:
            particular_parser = self.STATE_SCRAPER_MAP[state]()
            print(particular_parser)
            scraper_response: ScraperResponse = particular_parser.run(district, assemblyConstituency, pollingPart)
            return scraper_response
        except Exception as e:
            print(e)
            return None
        # self.translateParseElectoralRollPDF(scraper_response, state)

    def translateParseElectoralRollPDF(self, scraper_response, state):
        try:
            print("Parsing Electoral Roll PDF")
            pdf_file_path = scraper_response.electoral_roll_PDF if scraper_response else "scripts/pdf_to_txt/roll.pdf"
            pdf_parsed_response = None
            if self.STATE_LANGUAGE[state] == "en":
                print("Directly parsing PDF...")
                pdf_parsed_response = self.PDF_TO_TXT_PARSER.convert(pdf_file_path)
            else:
                print("Translating and parsing PDF...")
                pdf_parsed_response = self.PDF_TO_TXT_PARSER.convert_translated(pdf_file_path, self.STATE_LANGUAGE[state])
            print(pdf_parsed_response)
            return pdf_parsed_response
        except Exception as e:
            print(e)
            return None
        # self.generateDataCSV(pdf_parsed_response)

    def generateDataCSV(self, parsed_response):
        try:
            print("Generating Data CSV from parsed text")
            txt_file_path = parsed_response.parsed_text_generated if parsed_response else "scraper_parser_translator/views/pdf_to_txt/parsed.txt"
            csv_generated_response = parse_english(str(txt_file_path), "scraper_parser_translator/views/txt_to_csv/output.csv")
            print(csv_generated_response)
            return csv_generated_response
        except Exception as e:
            print(e)
            return None

    def csvToJsonPostAlgo(self, name, father_or_husband, father_or_husband_name, age):
        try:
            print("Generating JSON from created csv")
            exec_location = os.path.abspath(os.curdir)
            exec_location = str(exec_location) + "/scraper_parser_translator/views/relations/a.out"
            # father-1, husband-0
            # exec_location += " 'TARUN RAI' '1' 'HARKA BAHADUR RAI' '23'"
            print(exec_location)
            def make_json(csvFilePath, jsonFilePath):
                data = {}
                with open(csvFilePath, encoding='utf-8') as csvf:
                    csvReader = csv.DictReader(csvf)
                    for rows in csvReader:
                        key = rows['Id']
                        data[key] = rows
                return data
            csvFilePath = 'scraper_parser_translator/views/relations/Out.csv'
            jsonFilePath = 'scraper_parser_translator/views/relations/Out.json'
            # subprocess.run(exec_location)
            # subprocess.run([exec_location, "TARUN RAI", "1", "HARKA BAHADUR RAI", "23"])
            subprocess.run([exec_location, name, father_or_husband, father_or_husband_name, age])
            dict=make_json(csvFilePath, jsonFilePath)
            if(len(dict)==0):
                if(father_or_husband=="1"):
                    return {'0':{'Name':name,'Father\'s Name':father_or_husband_name}}
                else:
                    return {'0':{'Name':name,'Husband\'s Name':father_or_husband_name}}
            return dict
        except Exception as e:
            print(e)
            return None


# if __name__ == "__main__":
#     main_scraper = MainScraper()
#     # main_scraper.callParticularScraper("gujarat", None, None, None)
#     # res = main_scraper.translateElectoralRollPDF(None, "maharashtra")
#     main_scraper.csvToJsonPostAlgo()
        
