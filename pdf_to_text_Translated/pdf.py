from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import os
from googletrans import Translator

from PyPDF2 import PdfFileWriter, PdfFileReader

translator = Translator()
inputpdf = PdfFileReader("roll.pdf")
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


project_id = 'angular-port-366318'
location = 'us' # Format is 'us' or 'eu'
processor_id = 'd78cc8be15e93221' #  Create processor before running sample
file_path = os.path.abspath('DraftRoll-3-7.pdf')
mime_type = 'application/pdf' # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types

translated_text=""

def quickstart(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str,translated_text:str
):

    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project_id/locations/location/processor/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    # For a full list of Document object attributes, please reference this page:
    # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document
    document = result.document

    # Read the text recognition output from the processor
    print("The document contains the following text:")
    print(document.text)

    
    from_lang = 'gu'
    to_lang = 'en'

    #no of char in string
    #print(len(document.text))

    chars=len(document.text)

    trans=""
    for i in range(0,chars,5000):
        #print(i)
        #print(document.text[i:i+5000])

        translated = translator.translate(document.text[i:i+5000], src=from_lang, dest=to_lang)
        trans+=translated.text

    return trans

    

for i in range(noOfpdf+1):
    file_path = os.path.abspath('document-page%s.pdf' % i)
    translated_text+=quickstart(project_id, location, processor_id, file_path, mime_type,translated_text)

with open('translated.txt', 'w', encoding='utf-8') as f:
        f.write(translated_text)

