from django.shortcuts import render
from django.http import JsonResponse
from scraper_parser_translator.views.mainScraper import MainScraper
# from ..scraper_parser_translator.views.mainScraper import MainScraper

# class ControllerClass:
    # def __init__(self) -> None:
        # self.MAIN_SCRAPER = MainScraper()
MAIN_SCRAPER = MainScraper()
        
def home(request):
    print(request)
    return JsonResponse({"message": "Hey there"})

# Test sikkim
def sikkim(request):
    MAIN_SCRAPER.callParticularScraper("sikkim", None, None, None)
    return JsonResponse({"message": "Testing"})