from .scraperResponse import ScraperResponse
from .maharashtra.scraper import ScraperClass as MaharashtraScraper
from .gujarat.scraper import ScraperClass as GujuratScraper
from .goa.scraper import ScraperClass as GoaScraper
from .sikkim.scraper import ScraperClass as SikkimScraper
from .mizoram.scraper import ScraperClass as MizoramScraper
from .voter_portal.scraper import ScraperClass as VoterPortalScraper
from .pdf_to_txt.pdf import PDF_to_Txt
from .txt_to_csv.multi_lang_processing import parse_english
    

class MainScraper:
    def __init__(self) -> None:
        self.VOTER_PORTAL_SCRAPER = VoterPortalScraper
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

    def callVoterPortalDetailedSearch(self, ):
        scraper_response = self.VOTER_PORTAL_SCRAPER.
        

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
        txt_file_path = parsed_response.parsed_text_generated if parsed_response else "scripts/pdf_to_txt/parsed.txt"
        csv_generated_response = parse_english(str(txt_file_path), "scripts/txt_to_csv/output.csv")
        print(csv_generated_response)
        return csv_generated_response


if __name__ == "__main__":
    main_scraper = MainScraper()
    main_scraper.callParticularScraper("gujarat", None, None, None)
    # res = main_scraper.translateElectoralRollPDF(None, "maharashtra")
        
