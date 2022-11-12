import io
import os
# Imports the Google Cloud client library
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('Output_4.png')


with io.open(file_name, 'rb') as image_file:
        content = image_file.read()


image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')

for text in texts:
    print('\n"{}"'.format(text.description))
    text = '\n"{}"'.format(text.description)
    with open('testingPNG.txt', 'a') as f:
                f.write('\n')
                f.write(text)

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices])

    print('bounds: {}'.format(','.join(vertices)))

if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))