from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from ..scraperResponse import PdfOCRParserResponse
from pathlib import Path
from googletrans import Translator
import os

from PyPDF2 import PdfFileWriter, PdfFileReader

class PDF_to_Txt:
    def __init__(self) -> None:
        self.translator = Translator()
        self.language_to_code={
            'English':'en',
            'Hindi':'hi',
            'Gujarati':'gu',
            'Marathi':'mr',
            'Tamil':'ta',
            'Telugu':'te',
            'Kannada':'kn',
            'Malayalam':'ml',
            'Bengali':'bn',
            'Odia':'or',
            'Punjabi':'pa',
            'Assamese':'as'
        }
        self.project_id = 'angular-port-366318'
        self.location = 'us' # Format is 'us' or 'eu'
        self.processor_id = 'd78cc8be15e93221' #  Create processor before running sample
        self.file_path = os.path.abspath('DraftRoll-3-7.pdf')
        self.mime_type = 'application/pdf' # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
        # You must set the api_endpoint if you use a location other than 'us', e.g.:
        opts = ClientOptions(api_endpoint=f"{self.location}-documentai.googleapis.com", credentials_file="scripts/pdf_to_txt/keys.json")
        self.CLIENT = documentai.DocumentProcessorServiceClient(client_options=opts)
        # The full resource name of the processor, e.g.:
        # projects/project_id/locations/location/processor/processor_id
        self.CLIENT_NAME = self.CLIENT.processor_path(self.project_id, self.location, self.processor_id)
        self.CUSTOM_RESPONSE = PdfOCRParserResponse()


    def convert(self, file_name):
        input_file = file_name if file_name else "roll.pdf"
        inputpdf = PdfFileReader(input_file)
        offset=2
        noOfpdf= (inputpdf.numPages-offset)//10

        for i in range(noOfpdf+1):
            output = PdfFileWriter()
            no=1
            if i==noOfpdf:
                no=(inputpdf.numPages-offset)%10
            else:
                no=10
            for j in range(no):
                output.addPage(inputpdf.getPage(i+j+offset))
            with open("document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)

        translated_text=""
        def quickstart(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str,translated_text:str):
            # Read the file into memory
            with open(file_path, "rb") as image:
                image_content = image.read()
            # Load Binary Data into Document AI RawDocument Object
            raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
            # Configure the process request
            request = documentai.ProcessRequest(name=self.CLIENT_NAME, raw_document=raw_document)
            result = self.CLIENT.process_document(request=request)
            # For a full list of Document object attributes, please reference this page:
            # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document
            document = result.document
            # Read the text recognition output from the processor
            print("The document text is parsed:")
            # print(document.text)
            return document.text
        for i in range(noOfpdf+1):
            file_path = os.path.abspath('document-page%s.pdf' % i)
            translated_text=quickstart(self.project_id, self.location, self.processor_id, file_path, self.mime_type, translated_text)
            #write in file
        file_path = "scripts/pdf_to_txt/parsed.txt"
        self.CUSTOM_RESPONSE.parsed_text_generated = Path(file_path)
        with open(file_path, 'a') as f:
            f.write(translated_text)
        self.CUSTOM_RESPONSE.status = True
        return self.CUSTOM_RESPONSE

    def convert_translated(self, file_name, state_lang):
        input_file = file_name if file_name else "roll.pdf"
        inputpdf = PdfFileReader(input_file)
        offset=2
        noOfpdf= (inputpdf.numPages-offset)//10

        for i in range(noOfpdf+1):
            output = PdfFileWriter()
            no=1
            if i==noOfpdf:
                no=(inputpdf.numPages-offset)%10
            else:
                no=10
            for j in range(no):
                output.addPage(inputpdf.getPage(i+j+offset))
            with open("document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)

        translated_text=""
        def quickstart(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str,translated_text:str):
            with open(file_path, "rb") as image:
                image_content = image.read()
            # Load Binary Data into Document AI RawDocument Object
            raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
            # Configure the process request
            request = documentai.ProcessRequest(name=self.CLIENT_NAME, raw_document=raw_document)
            result = self.CLIENT.process_document(request=request)
            # For a full list of Document object attributes, please reference this page:
            # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document
            document = result.document
            # Read the text recognition output from the processor
            print("The document text is parsed and translated.")
            # print(document.text)
            from_lang = state_lang if state_lang else 'gu'
            to_lang = 'en'
            #no of char in string
            #print(len(document.text))
            chars=len(document.text)
            trans=""
            for i in range(0,chars,5000):
                #print(i)
                #print(document.text[i:i+5000])
                translated = self.translator.translate(document.text[i:i+5000], src=from_lang, dest=to_lang)
                trans+=translated.text
            return trans    

        for i in range(noOfpdf+1):
            file_path = os.path.abspath('document-page%s.pdf' % i)
            translated_text += quickstart(self.project_id, self.location, self.processor_id, file_path, self.mime_type,translated_text)

        file_path = "scripts/pdf_to_txt/parsed_translated.txt"
        self.CUSTOM_RESPONSE.parsed_text_generated = Path(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(translated_text)
        self.CUSTOM_RESPONSE.status = True
        return self.CUSTOM_RESPONSE


# if __name__ == "__main__":
#     pdf_to_txt = PDF_to_Txt()
#     resp = pdf_to_txt.convert("scripts/pdf_to_txt/roll.pdf")
#     print(resp)
