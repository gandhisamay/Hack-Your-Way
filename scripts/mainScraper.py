from .scraperResponse import ScraperResponse
from .maharashtra.scraper import ScraperClass as MaharashtraScraper
from .gujarat.scraper import ScraperClass as GujuratScraper
from .goa.scraper import ScraperClass as GoaScraper
from .sikkim.scraper import ScraperClass as SikkimScraper
from .mizoram.scraper import ScraperClass as MizoramScraper
from .pdf_to_txt.pdf import PDF_to_Txt
    

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
        self.translateElectoralRollPDF(scraper_response, state)

    def translateElectoralRollPDF(self, scraper_response, state):
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


if __name__ == "__main__":
    main_scraper = MainScraper()
    main_scraper.callParticularScraper("gujarat", None, None, None)
    # res = main_scraper.translateElectoralRollPDF(None, "maharashtra")
        
