
import io
import os

from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
client = vision.ImageAnnotatorClient()


def detect_text(path):
    """Detects text in the file."""

    with io.open(os.path.realpath(path), 'rb') as image_file:
        content = image_file.read()

    return detect_text_swagger(content)

def detect_text_swagger(content):
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    '''for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    '''
    

    return ('\n"{}"'.format(texts[0].description)).strip()
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


