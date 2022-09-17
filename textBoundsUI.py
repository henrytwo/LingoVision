from pygame import *
from PIL import Image
import io

init()

WIDTH = 1920 #1200
HEIGHT = 1080 #675

def textBoundDebug(img, boxes, targetted_box):
    with open(img, 'rb') as file:
        result = swaggertextBoundDebug(file, boxes, targetted_box)

        image.save(result, "screenshot.jpeg")
def swaggertextBoundDebug(img, boxes, targetted_box):
    pil_image = Image.open(io.BytesIO(img))

    screen = display.set_mode((1, 1))

    captureImg = image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode).convert()
    captureImg = transform.scale(captureImg, (WIDTH, HEIGHT))

    for box in boxes:
        draw.polygon(captureImg, (0, 255, 0), box, 2)

    draw.polygon(captureImg, (255, 0, 0), targetted_box, 2)

    temp_io = io.BytesIO()
    image.save(captureImg, temp_io, "JPEG")

    return temp_io.read()
