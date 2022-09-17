from pygame import *

init()

WIDTH = 1920 #1200
HEIGHT = 1080 #675

def textBoundDebug(img, boxes, targetted_box):
    result = swaggertextBoundDebug(img, boxes, targetted_box)

    image.save(result, "screenshot.jpeg")
def swaggertextBoundDebug(img, boxes, targetted_box):
    captureImg = image.load(img)
    captureImg = transform.scale(captureImg, (WIDTH, HEIGHT))

    for box in boxes:
        draw.polygon(captureImg, (0, 255, 0), box, 2)

    draw.polygon(captureImg, (255, 0, 0), targetted_box, 2)

    temp_io = io.BytesIO()
    image.save(captureImg, temp_io, "JPEG")

    return temp_io
