import os
import csv
import json
import subprocess
from .scraperResponse import ScraperResponse
from .maharashtra.scraper import ScraperClass as MaharashtraScraper
from .gujarat.scraper import ScraperClass as GujuratScraper
from .goa.scraper import ScraperClass as GoaScraper
from .sikkim.scraper import ScraperClass as SikkimScraper
from .mizoram.scraper import ScraperClass as MizoramScraper
from .pdf_to_txt.pdf import PDF_to_Txt
from .txt_to_csv.multi_lang_processing import parse_english
    

class MainScraper:
    def __init__(self) -> None:
        self.STATE_SCRAPER_MAP = {"maharashtra": MaharashtraScraper,
            "gujarat": GujuratScraper,
            "goa": GoaScraper,
            "sikkim": SikkimScraper,
            "mizoram": MizoramScraper}
        self.STATE_LANGUAGE = {"maharashtra": "mr",
            "gujarat": "gu",
            "goa": "en",
            "sikkim": "en",
            "mizoram": "en"}
        self.PDF_TO_TXT_PARSER = PDF_to_Txt()

    def callParticularScraper(self, state, district, assemblyConstituency, pollingPart):
        particular_parser = self.STATE_SCRAPER_MAP[state]()
        scraper_response: ScraperResponse = particular_parser.run(district, assemblyConstituency, pollingPart)
        print(scraper_response)
        self.translateParseElectoralRollPDF(scraper_response, state)

    def translateParseElectoralRollPDF(self, scraper_response, state):
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
        # return pdf_parsed_response
        self.generateDataCSV(pdf_parsed_response)

    def generateDataCSV(self, parsed_response):
        print("Generating Data CSV from parsed text")
        txt_file_path = parsed_response.parsed_text_generated if parsed_response else "scraper_parser_translator/views/pdf_to_txt/parsed.txt"
        csv_generated_response = parse_english(str(txt_file_path), "scraper_parser_translator/views/txt_to_csv/output.csv")
        print(csv_generated_response)
        return csv_generated_response

    def csvToJsonPostAlgo(self):
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
            with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
                jsonf.write(json.dumps(data, indent=4))
        csvFilePath = 'scraper_parser_translator/views/relations/Out.csv'
        jsonFilePath = 'scraper_parser_translator/views/relations/Out.json'
        # subprocess.run(exec_location)
        subprocess.run([exec_location, "TARUN RAI", "1", "HARKA BAHADUR RAI", "23"])
        make_json(csvFilePath, jsonFilePath)


if __name__ == "__main__":
    main_scraper = MainScraper()
    # main_scraper.callParticularScraper("gujarat", None, None, None)
    # res = main_scraper.translateElectoralRollPDF(None, "maharashtra")
    main_scraper.csvToJsonPostAlgo()
        
