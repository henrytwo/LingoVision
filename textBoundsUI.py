from pygame import *

init()

def textBoundDebug(img, boxes, targetted_box):
    captureImg = image.load(img)

    screen = display.set_mode([captureImg.get_width(), captureImg.get_height()])
    running = True

    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        screen.blit(captureImg, (0, 0))

        for box in boxes:
            draw.polygon(screen, (0, 255, 0), box, 2)

        draw.polygon(screen, (255, 0, 0), targetted_box, 2)

        display.flip()

        image.save(screen, "screenshot.jpeg")

        break

    quit()

