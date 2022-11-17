from django.http import JsonResponse
from .mainScraper import MainScraper
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
from .scraperResponse import UserInput, VoterPortalResponse, JSONClassEncoder
from .middleware import RequestUniqueID
# from ..scraper_parser_translator.views.mainScraper import MainScraper

# class ControllerClass:
    # def __init__(self) -> None:
        # self.MAIN_SCRAPER = MainScraper()
MAIN_SCRAPER = MainScraper()
json_class_encoder = JSONClassEncoder()
REQUEST_MEDIA_HOME = "scraper_parser_translator/requests_data/"
        
@csrf_exempt
def home(request):
    print(f"Printing Request's unique ID: {request.META.get('uuid')}")
    return JsonResponse({"message": "Follow the below URLs (POST) for obtaining relevant data.", 
                            "Detailed_Search": "/api/details", 
                            "Epic_Search": "/api/epic"})

# TODO: DOB?
@csrf_exempt
def details(request):
    request_media_dir = REQUEST_MEDIA_HOME + str(request.META.get('uuid')) + "/"
    subprocess.run(["mkdir", "-p", request_media_dir])
    print(f">>> Created Requests MEDIA DATA DIRECTORY at: {request_media_dir}")
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
        print(input_data)
        #  getting main portal response
 
        subprocess.run(["node", "scraper_parser_translator/views/voter_portal_js/index.js", 
                        "detailedSearch",
                        request_media_dir,
                        input_data.name,
                        input_data.father_or_husband_name,
                        input_data.age,
                        input_data.gender,
                        input_data.state,
                        input_data.district if input_data.district else "0",
                        input_data.assembly_constituency if input_data.assembly_constituency else "0"])
        # Opening JSON file
        voter_portal_response = None
        with open(request_media_dir + "data.json") as json_file:
            data = json.load(json_file)
            print(f"Data from Main Portal: {data}")
            print(data["found"] == True)
            if data["found"] == True:
                voter_portal_response = VoterPortalResponse()
                voter_portal_response.epic_no                         = data["epicNo"]
                voter_portal_response.state                           = input_data.state
                voter_portal_response.name                            = data["name"]
                voter_portal_response.age                             = data["age"]
                voter_portal_response.gender                          = data["gender"]
                voter_portal_response.father_or_husband_name          = data["fatherOrHusbandName"]
                voter_portal_response.district                        = data["district"]
                voter_portal_response.assembly_constituency_no        = data["ac_no"]
                voter_portal_response.assembly_constituency_name      = data["ac_name"]
                voter_portal_response.parliamentary_constituency_name = data["pc_name"]
                voter_portal_response.polling_station_name            = data["ps_name"]
                voter_portal_response.part_number                     = data["part_no"]
        #voter_portal_response = MAIN_SCRAPER.callVoterPortal(False, input_data)
        print(voter_portal_response)
    
        if voter_portal_response != None:
            # return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again.", 
            #                     "data": json_class_encoder.encode(voter_portal_response)})
            particular_portal_response = MAIN_SCRAPER.callParticularScraper(input_data.state, 
                                            voter_portal_response.district, 
                                            f"{voter_portal_response.assembly_constituency_name}-{voter_portal_response.assembly_constituency_no}",
                                            voter_portal_response.part_number,
                                            request_media_dir)
            print(particular_portal_response)
        else:
            # particular_portal_response = MAIN_SCRAPER.callParticularScraper("Sikkim", 
            #                                 "North Goa", 
            #                                 "Porvorim-9",
            #                                 "16")
            # input_data.name = "Deepali"
            # input_data.father_or_husband = True
            # input_data.father_or_husband_name = "Laximan Naik"
            # input_data.age = "26"
            # input_data.gender = "M"
            # print(particular_portal_response)
            print("Cleaning Request Media Data directory...")
            subprocess.run(["rm", "-rf", request_media_dir])
            print(f"Cleared Directory: {request_media_dir}")
            return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again."})

        if particular_portal_response != None:
            # return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again.", 
            #                     "data": json_class_encoder.encode(particular_portal_response)})
            translated_parsed_response = MAIN_SCRAPER.translateParseElectoralRollPDF(particular_portal_response, input_data.state)
            print(translated_parsed_response)
        else:
            print("Cleaning Request Media Data directory...")
            subprocess.run(["rm", "-rf", request_media_dir])
            print(f"Cleared Directory: {request_media_dir}")
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        if translated_parsed_response != None:
            # return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again.", 
            #                     "data": json_class_encoder.encode(particular_portal_response)})
            generated_csv_data = MAIN_SCRAPER.generateDataCSV(translated_parsed_response)
            print(generated_csv_data)
        else:
            print("Cleaning Request Media Data directory...")
            subprocess.run(["rm", "-rf", request_media_dir])
            print(f"Cleared Directory: {request_media_dir}")
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        if generated_csv_data != None:
            # return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again.", 
            #                     "data": json_class_encoder.encode(particular_portal_response)})
            final_response = MAIN_SCRAPER.csvToJsonPostAlgo(input_data.name, 
                                                            "1" if input_data.father_or_husband else "0", 
                                                            input_data.father_or_husband_name,
                                                            input_data.age,
                                                            request_media_dir)
            print(final_response)
        else:
            print("Cleaning Request Media Data directory...")
            subprocess.run(["rm", "-rf", request_media_dir])
            print(f"Cleared Directory: {request_media_dir}")
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        print("Cleaning Request Media Data directory...")
        subprocess.run(["rm", "-rf", request_media_dir])
        print(f"Cleared Directory: {request_media_dir}")
        return JsonResponse({"message": "Successfull", "data": final_response})

@csrf_exempt
def epic(request):
    request_media_dir = REQUEST_MEDIA_HOME + str(request.META.get('uuid')) + "/"
    subprocess.run(["mkdir", "-p", request_media_dir])
    print(f">>> Created Requests MEDIA DATA DIRECTORY at: {request_media_dir}")
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
        print(input_data)
        voter_portal_response = None
        subprocess.run(["node", "scraper_parser_translator/views/voter_portal_js/index.js", 
                        "epic_search",
                        request_media_dir,
                        input_data.epic_no,
                        input_data.state])
        # Opening JSON file
        with open(request_media_dir + "data.json") as json_file:
            data = json.load(json_file)
            print(f"Data from Main Portal: {data}")
            print(data["found"] == True)
            if data["found"] == True:
                voter_portal_response = VoterPortalResponse()
                voter_portal_response.epic_no                         = input_data.epic_no
                voter_portal_response.state                           = input_data.state
                voter_portal_response.name                            = data["name"]
                voter_portal_response.age                             = data["age"]
                voter_portal_response.gender                          = data["gender"]
                voter_portal_response.father_or_husband_name          = data["fatherOrHusbandName"]
                voter_portal_response.district                        = data["district"]
                voter_portal_response.assembly_constituency_no        = data["ac_no"]
                voter_portal_response.assembly_constituency_name      = data["ac_name"]
                voter_portal_response.parliamentary_constituency_name = data["pc_name"]
                voter_portal_response.polling_station_name            = data["ps_name"]
                voter_portal_response.part_number                     = data["part_no"]
        # voter_portal_response = MAIN_SCRAPER.callVoterPortal(True, input_data)
        print(voter_portal_response)
        if voter_portal_response:
            input_data.name = voter_portal_response.name
            input_data.state = voter_portal_response.state
            input_data.age = voter_portal_response.age
            input_data.father_or_husband_name = voter_portal_response.father_or_husband_name
            # input_data.father_or_husband = True
    
        if voter_portal_response != None:
            # return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again.", 
            #                     "data": json_class_encoder.encode(voter_portal_response)})
            particular_portal_response = MAIN_SCRAPER.callParticularScraper(voter_portal_response.state, 
                                            voter_portal_response.district, 
                                            f"{voter_portal_response.assembly_constituency_name}-{voter_portal_response.assembly_constituency_no}",
                                            voter_portal_response.part_number,
                                            request_media_dir)
            print(particular_portal_response)
        else:
            # particular_portal_response = MAIN_SCRAPER.callParticularScraper("Sikkim", 
            #                                 "Sikkim", 
            #                                 "RINCHENPONG-5",
            #                                 "1")
            # input_data.name = "NAK TSH LEPCHA"
            # input_data.father_or_husband = True
            # input_data.father_or_husband_name = "BIMAL SUBBA"
            # input_data.age = "53"
            # input_data.gender = "M"
            # print(particular_portal_response)
            print("Cleaning Request Media Data directory...")
            subprocess.run(["rm", "-rf", request_media_dir])
            print(f"Cleared Directory: {request_media_dir}")
            return JsonResponse({"message": "Sorry, the main NSVP Portal couldn't be reached at the moment, please try again."})

        if particular_portal_response != None:
            translated_parsed_response = MAIN_SCRAPER.translateParseElectoralRollPDF(particular_portal_response, input_data.state)
            print(translated_parsed_response)
        else:
            print("Cleaning Request Media Data directory...")
            subprocess.run(["rm", "-rf", request_media_dir])
            print(f"Cleared Directory: {request_media_dir}")
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        if translated_parsed_response != None:
            generated_csv_data = MAIN_SCRAPER.generateDataCSV(translated_parsed_response)
            print(generated_csv_data)
        else:
            print("Cleaning Request Media Data directory...")
            subprocess.run(["rm", "-rf", request_media_dir])
            print(f"Cleared Directory: {request_media_dir}")
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        if generated_csv_data != None:
            final_response = MAIN_SCRAPER.csvToJsonPostAlgo(input_data.name, 
                                                            "1" if input_data.father_or_husband else "0", 
                                                            input_data.father_or_husband_name,
                                                            input_data.age,
                                                            request_media_dir)
            print(final_response)
        else:
            print("Cleaning Request Media Data directory...")
            subprocess.run(["rm", "-rf", request_media_dir])
            print(f"Cleared Directory: {request_media_dir}")
            return JsonResponse({"message": "Sorry, the google document ai service for translation is not up, please try again."})

        print("Cleaning Request Media Data directory...")
        subprocess.run(["rm", "-rf", request_media_dir])
        print(f"Cleared Directory: {request_media_dir}")
        return JsonResponse({"message": "Successfull", "data": final_response})
        # MAIN_SCRAPER.callParticularScraper("sikkim", None, None, None)
