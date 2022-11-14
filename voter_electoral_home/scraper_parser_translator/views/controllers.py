from django.shortcuts import render
from django.http import JsonResponse
from .mainScraper import MainScraper
from django.views.decorators.csrf import csrf_exempt
import json
from .scraperResponse import UserInput
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
        input_data = UserInput()
        body_unicode = request.body.decode('utf-8')
        req_body = json.loads(body_unicode)
        try:
            if "name" in req_body:
                input_data.name = str(req_body["name"])
            else: raise ValueError()
            if "age" in req_body:
                input_data.age = str(req_body["age"])
            else: raise ValueError()
            if "gender" in req_body:
                input_data.gender = str(req_body["gender"])
            else: raise ValueError()
            if "state" in req_body:
                input_data.state = str(req_body["state"])
            else: raise ValueError()
            if "father_or_husband_name" in req_body:
                input_data.father_or_husband_name = str(req_body["father_or_husband_name"])
            else: raise ValueError()
            if "father_or_husband" in req_body:
                input_data.father_or_husband = bool(req_body["father_or_husband"])
            else: raise ValueError()
            input_data.district = str(req_body["district"]) if "district" in req_body else None
            input_data.assembly_constituency = str(req_body["assembly_constituency"]) if "assembly_constituency" in req_body else None
            input_data.epic_no = str(req_body["epic_no"]) if "epic_no" in req_body else None
        except:
            return JsonResponse({"message": f"Your request does not conform to the required format"})
        voter_portal_response = MAIN_SCRAPER.callVoterPortal(False, input_data)
        print(voter_portal_response)
    
        if voter_portal_response != None:
            particular_portal_response = MAIN_SCRAPER.callParticularScraper(input_data.state, 
                                            voter_portal_response.district, 
                                            f"{voter_portal_response.assembly_constituency_name}-{voter_portal_response.assembly_constituency_no}",
                                            voter_portal_response.part_number)
            print(particular_portal_response)
        else:
            return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again."})

        if particular_portal_response != None:
            translated_parsed_response = MAIN_SCRAPER.translateParseElectoralRollPDF(particular_portal_response, voter_portal_response.state)
            print(translated_parsed_response)
        else:
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        if translated_parsed_response != None:
            generated_csv_data = MAIN_SCRAPER.generateDataCSV(translated_parsed_response)
            print(generated_csv_data)
        else:
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        if generated_csv_data != None:
            final_response = MAIN_SCRAPER.csvToJsonPostAlgo(input_data.name, 
                                                            "1" if input_data.father_or_husband else "0", 
                                                            input_data.father_or_husband_name,
                                                            input_data.age)
            print(final_response)
        else:
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        return JsonResponse({"message": "Successfull", "data": final_response})

@csrf_exempt
def epic(request):
    if request.method == "GET":
        return JsonResponse({"message": "Please make a POST Request with Citizen's EPIC No!"})
    elif request.method == "POST":
        print("Post request called: Epic. . .")
        input_data = UserInput()
        body_unicode = request.body.decode('utf-8')
        req_body = json.loads(body_unicode)
        try:
            if "epic_no" in req_body:
                input_data.epic_no = str(req_body["epic_no"])
            else: raise ValueError()
            if "state" in req_body:
                input_data.state = str(req_body["state"])
            else: raise ValueError()
        except:
            return JsonResponse({"message": f"Your request does not conform to the required format"})
        voter_portal_response = None
        voter_portal_response = MAIN_SCRAPER.callVoterPortal(True, input_data)
        print(voter_portal_response)
    
        if voter_portal_response != None:
            particular_portal_response = MAIN_SCRAPER.callParticularScraper(voter_portal_response.state, 
                                            voter_portal_response.district, 
                                            f"{voter_portal_response.assembly_constituency_name}-{voter_portal_response.assembly_constituency_no}",
                                            voter_portal_response.part_number)
            print(particular_portal_response)
        else:
            # particular_portal_response = MAIN_SCRAPER.callParticularScraper("Mizoram", 
            #                                 "MAMIT", 
            #                                 "DAMPA-2",
            #                                 "1")
            # input_data.name = "Lalruatkimi"
            # input_data.father_or_husband = True
            # input_data.father_or_husband_name = "Lalramthara"
            # input_data.age = "25"
            # input_data.gender = "F"
            # print(particular_portal_response)
            return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again."})

        if particular_portal_response != None:
            translated_parsed_response = MAIN_SCRAPER.translateParseElectoralRollPDF(particular_portal_response, input_data.state)
            print(translated_parsed_response)
        else:
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        if translated_parsed_response != None:
            generated_csv_data = MAIN_SCRAPER.generateDataCSV(translated_parsed_response)
            print(generated_csv_data)
        else:
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        if generated_csv_data != None:
            final_response = MAIN_SCRAPER.csvToJsonPostAlgo(input_data.name, 
                                                            "1" if input_data.father_or_husband else "0", 
                                                            input_data.father_or_husband_name,
                                                            input_data.age)
            print(final_response)
        else:
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        return JsonResponse({"message": "Successfull", "data": final_response})
        # MAIN_SCRAPER.callParticularScraper("sikkim", None, None, None)
