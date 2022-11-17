import io
import os
import sys
# Imports the Google Cloud client library
from google.cloud import vision
from google.oauth2 import service_account

class Captcha_To_Txt:
    def __init__(self, STATE: str, req_dir: str) -> None:
        # The name of the image file to annotate
        self.FILE_NAME = req_dir
        self.CAPTCHA_LOCATION = "captcha.png"
        # + os.path.abspath('captcha.png')
        # self.FILE_NAME = os.path.join(self.FILE_NAME, "scraper_parser_translator/views", STATE, self.CAPTCHA_LOCATION)
        self.FILE_NAME += self.CAPTCHA_LOCATION
        print(self.FILE_NAME)
        # Instantiates a client
        credentials = service_account.Credentials.from_service_account_file('keys.json')

        # Instantiates a client
        self.CLIENT = vision.ImageAnnotatorClient(credentials=credentials)
        with io.open(self.FILE_NAME, 'rb') as image_file:
            content = image_file.read()
        self.IMAGE = vision.Image(content=content)
        
    def get(self, voter_portal: bool = False) -> str:
        # get response
        response = self.CLIENT.text_detection(image=self.IMAGE)
        texts = response.text_annotations
        # print('Texts:\n\n')
        CAPTCHA_TEXT = texts[0].description
        print(f"CAPTCHA TEXT = {CAPTCHA_TEXT}")
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        if voter_portal:
            self.CAPTCHA_TEXT_LOCATION = self.FILE_NAME.rsplit("/", 1)[0] + "/captcha_text"
            with io.open(self.CAPTCHA_TEXT_LOCATION, 'w') as file:
                file.write(CAPTCHA_TEXT)
            print(f"Captcha text `{CAPTCHA_TEXT}` stored at: {self.CAPTCHA_TEXT_LOCATION}")
        return CAPTCHA_TEXT

def main(state: str, req_dir: str, voter_portal: bool = False):
    ctt = Captcha_To_Txt(state, req_dir)
    return ctt.get(voter_portal)

if __name__ == "__main__":
    # print(sys.argv)
    response = main("voter_portal", sys.argv[1], voter_portal=True)
    print(response)

# for text in texts:
#     print('\n"{}"'.format(text.description))
#
#     vertices = (['({},{})'.format(vertex.x, vertex.y)
#                 for vertex in text.bounding_poly.vertices])
#
#     print('bounds: {}'.format(','.join(vertices)))

