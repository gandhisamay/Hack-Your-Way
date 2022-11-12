from .maharashtra.scraper import ScraperClass as MaharashtraScraper
from .gujarat.scraper import ScraperClass as GujuratScraper
from .goa.scraper import ScraperClass as GoaScraper
    

class MainScraper:
    def __init__(self) -> None:
        self.MAP = {"maharashtra": MaharashtraScraper, "gujarat": GujuratScraper, "goa": GoaScraper}
        pass

    def callParticularParser(self, state, district, assemblyConstituency, pollingPart):
        particular_parser = self.MAP[state]()
        particular_parser.run(district, assemblyConstituency, pollingPart)


if __name__ == "__main__":
    main_scraper = MainScraper()
    main_scraper.callParticularParser("goa", None, None, None)
        
