from pathlib import Path

class VoterPortalResponse:
    def __init__(self):
        self.epic_no = "Not instantiated"
        self.name = "Not instantiated"
        self.gender = "Not instatiated"
        self.age = "Not instantiated"
        self.father_or_husband_name = "Not instantiated"
        self.state = "Not instatiated"
        self.district = "Not instatiated"
        self.assembly_constituency_no = "Not instantiated"
        self.assembly_constituency_name ="Not instantiated"
        self.polling_station_name = "Not instantiated"
        self.parliamentary_constituency_name = "Not instantiated" 
        self.part_number = "Not instantiated"

    def __str__(self) -> str:
        return f"EPIC NUMBER: {self.epic_no}\n \
        NAME: {self.name}\n \
        GENDER: {self.gender}\n \
        AGE: {self.age}\n \
        FATHER_OR_HUSBAND_NAME: {self.father_or_husband_name}\n \
        STATE: {self.state}\n \  " 

        

class ScraperResponse:
    def __init__(self) -> None:
        self.status: bool = False
        self.message: str = "Not instantiated"
        self.captcha_generated: Path | None = None
        self.electoral_roll_PDF: Path = Path(__file__).parent

    def __str__(self) -> str:
        return f"STATUS: {self.status}\n \
        MESSAGE: {self.message}\n \
        CAPTCHA_LOCATION: {self.captcha_generated}\n \
        ELECTORAL_ROLL_LOCATION: {self.electoral_roll_PDF}\n"


class CsvGenerateResponse:
    def __init__(self) -> None:
        self.status: bool = False
        self.message: str = "Not instantiated"
        self.csv_generated: Path | None = None

    def __str__(self) -> str:
        return f"STATUS: {self.status}\n \
        MESSAGE: {self.message}\n \
        CSV_GENERATED: {self.csv_generated}\n"


class PdfOCRParserResponse:
    def __init__(self) -> None:
        self.status: bool = False
        self.message: str = "Not instantiated"
        self.parsed_text_generated: Path | None = None

    def __str__(self) -> str:
        return f"STATUS: {self.status}\n \
        MESSAGE: {self.message}\n \
        PARSED_TEXT_GENERATED: {self.parsed_text_generated}\n"

# if __name__ == "__main__":
#     scraper_reponse = ScraperResponse()
