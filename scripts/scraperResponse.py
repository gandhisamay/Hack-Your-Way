from pathlib import Path

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
