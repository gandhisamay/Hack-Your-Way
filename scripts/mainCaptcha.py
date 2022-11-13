import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
from google.oauth2 import service_account

class Captcha_To_Txt:
    def __init__(self, STATE: str) -> None:
        # The name of the image file to annotate
        self.FILE_NAME = os.path.abspath('.')
        self.CAPTCHA_LOCATION = "captcha.png"
        # + os.path.abspath('captcha.png')
        self.FILE_NAME = os.path.join(self.FILE_NAME, "scripts", STATE, self.CAPTCHA_LOCATION)
        print(self.FILE_NAME)
        # Instantiates a client
        credentials = service_account.Credentials.from_service_account_file(
            'keys.json')

        # Instantiates a client
        self.CLIENT = vision.ImageAnnotatorClient(credentials=credentials)
        with io.open(self.FILE_NAME, 'rb') as image_file:
            content = image_file.read()
        self.IMAGE = vision.Image(content=content)
        
    def get(self) -> str:
        # get response
        response = self.CLIENT.text_detection(image=self.IMAGE)
        texts = response.text_annotations
        print(texts)
        # print('Texts:\n\n')
        CAPTCHA_TEXT = texts[0].description
        # print(f"CAPTCHA TEXT = {CAPTCHA_TEXT}")
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        return CAPTCHA_TEXT

def main(state: str):
    ctt = Captcha_To_Txt(state)
    return ctt.get()

if __name__ == "__main__":
    response = main("maharashtra")
    print(response)

# for text in texts:
#     print('\n"{}"'.format(text.description))
#
#     vertices = (['({},{})'.format(vertex.x, vertex.y)
#                 for vertex in text.bounding_poly.vertices])
#
#     print('bounds: {}'.format(','.join(vertices)))

