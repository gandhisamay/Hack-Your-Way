from pathlib import Path
from json import JSONEncoder

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


class UserInput:
    def __init__(self) -> None:
        self.name: str = ""
        self.father_or_husband = True
        self.father_or_husband_name: str = ""
        self.gender: str = "M"
        self.age: str = "18"
        self.state: str = "Sikkim"
        self.epic_no = None
        self.district = None
        self.assembly_constituency = None

    def __str__(self) -> str:
        return f"EPIC NUMBER: {self.epic_no}\n \
        NAME: {self.name}\n \
        GENDER: {self.gender}\n \
        AGE: {self.age}\n \
        FATHER_OR_HUSBAND_NAME: {self.father_or_husband_name}\n \
        FATHER_OR_HUSBAND: {self.father_or_husband}\n \
        STATE: {self.state}\n \
        DISTRICT: {self.district}\n \
        ASSEMBLYCONSTITUENCY: {self.assembly_constituency}\n" 


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


class VoterPortalResponse:
    def __init__(self):
        self.epic_no = "Not instantiated"
        self.name = "Not instantiated"
        self.gender = "Not instatiated"
        self.age = "Not instantiated"
        self.father_or_husband_name = "Not instantiated"
        self.state = "Not instatiated" # NEEDED
        self.district = "Not instatiated" # DISTRICT
        self.assembly_constituency_no = "Not instantiated"
        self.assembly_constituency_name ="Not instantiated" # NEEDED
        self.polling_station_name = "Not instantiated"
        self.parliamentary_constituency_name = "Not instantiated"
        self.part_number = "Not instantiated" # NEEDED

    def __str__(self) -> str:
        return f"EPIC NUMBER: {self.epic_no}\n \
        NAME: {self.name}\n \
        GENDER: {self.gender}\n \
        AGE: {self.age}\n \
        FATHER_OR_HUSBAND_NAME: {self.father_or_husband_name}\n \
        STATE: {self.state}\n \
        DISTRICT: {self.district}\n \
        AC_NO: {self.assembly_constituency_no}\n \
        AC_NAME: {self.assembly_constituency_name}\n \
        POLLING_NAME: {self.polling_station_name}\n \
        PAR_CON_NAME: {self.parliamentary_constituency_name} \n \
        PART_NO: {self.part_number}\n " 


# subclass JSONEncoder
class JSONClassEncoder(JSONEncoder):
        def default(self, objectInstance):
            return objectInstance.__dict__

# if __name__ == "__main__":
#     scraper_reponse = ScraperResponse()
