
import io
import os
import json


from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
client = vision.ImageAnnotatorClient()


def detect_box(image, x, y) :
    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation

    boxes = []
    targetted_box = [[0, 0], [0, 0], [0, 0], [0, 0]]

    foundBox = False

    for page in texts.pages :
        for block in page.blocks:
            for paragraph in block.paragraphs:

                bounding = []

                for vertex in paragraph.bounding_box.vertices:
                    bounding.append([vertex.x, vertex.y])

                x1 = min([bounding[0][0], bounding[1][0], bounding[2][0], bounding[3][0]])
                x2 = max([bounding[0][0], bounding[1][0], bounding[2][0], bounding[3][0]])
                y1 = min([bounding[0][1], bounding[1][1], bounding[2][1], bounding[3][1]])
                y2 = max([bounding[0][1], bounding[1][1], bounding[2][1], bounding[3][1]])

                if (not foundBox) and x >= x1 and x <= x2 and y >= y1 and y <= y2 :
                    targetted_box = bounding
                    foundBox = True


                boxes.append(bounding)


    return boxes, targetted_box




def detect_overlap(A, B) :

    xa1 = min([A[0][0], A[1][0], A[2][0], A[3][0]])
    xa2 = max([A[0][0], A[1][0], A[2][0], A[3][0]])
    ya1 = min([A[0][1], A[1][1], A[2][1], A[3][1]])
    ya2 = max([A[0][1], A[1][1], A[2][1], A[3][1]])

    xb1 = min([B[0][0], B[1][0], B[2][0], B[3][0]])
    xb2 = max([B[0][0], B[1][0], B[2][0], B[3][0]])
    yb1 = min([B[0][1], B[1][1], B[2][1], B[3][1]])
    yb2 = max([B[0][1], B[1][1], B[2][1], B[3][1]])

    return ((xa1 <= xb1 and xb1 <= xa2) or (xa1 <= xb2 and xb2 <= xa2)) and ((ya1 <= yb1 and yb1 <= ya2) or (ya1 <= yb2 and yb2 <= ya2))



def detect_text(path):
    """Detects text in the file."""

    with io.open(os.path.realpath(path), 'rb') as image_file:
        content = image_file.read()

    return detect_text_swagger(content)

def detect_text_swagger(content):
    image = vision.Image(content=content)


    boxes, targetted_box = detect_box(image, 980, 470) #targetted box of text


    '''
    ####################################################
    with open('debugData.txt', 'w') as f:
        f.write(str(texts))
    ####################################################
    '''


    response = client.text_detection(image=image)
    texts = response.text_annotations
    texts = texts[1:]

    with open('debugData.txt', 'w') as f:
        f.write(str(texts))

    outputText = []

    for text in texts:

        bounding = []

        for vertex in text.bounding_poly.vertices :
            bounding.append([vertex.x, vertex.y])

        word = '\n"{}"'.format(text.description).strip()
        word = word[1:-1]

        if(detect_overlap(targetted_box, bounding)) :
            outputText.append(word)


    return " ".join(outputText), boxes, targetted_box

    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


    #return descs, bounds



