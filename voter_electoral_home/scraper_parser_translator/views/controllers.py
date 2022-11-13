from django.shortcuts import render
from django.http import JsonResponse
from .mainScraper import MainScraper
from django.views.decorators.csrf import csrf_exempt
# from ..scraper_parser_translator.views.mainScraper import MainScraper

# class ControllerClass:
    # def __init__(self) -> None:
        # self.MAIN_SCRAPER = MainScraper()
MAIN_SCRAPER = MainScraper()
        
@csrf_exempt
def home(request):
    print(request)
    return JsonResponse({"message": "Hey there >"})

# TODO: DOB?
@csrf_exempt
def details(request):
    if request.method == "GET":
        return JsonResponse({"message": "Please make a POST Request with Citizen's data!"})
    elif request.method == "POST":
        # MAIN_SCRAPER.callParticularScraper("sikkim", None, None, None)
        print("Post request called: Details. . .")
        print(request.body)
        return JsonResponse({"message": "Testing"})

@csrf_exempt
def epic(request):
    if request.method == "GET":
        return JsonResponse({"message": "Please make a POST Request with Citizen's EPIC No!"})
    elif request.method == "POST":
        # MAIN_SCRAPER.callParticularScraper("sikkim", None, None, None)
        print("Post request called: EPIC. . .")
        print(request.body)
        return JsonResponse({"message": "Testing"})
