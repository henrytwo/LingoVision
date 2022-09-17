from pygame import *

init()

WIDTH = 1920  # 1200
HEIGHT = 1080  # 675


def textBoundDebug(img, boxes, targetted_box):
    screen = display.set_mode([WIDTH, HEIGHT])
    running = True

    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        captureImg = image.load(img)
        captureImg = transform.scale(captureImg, (WIDTH, HEIGHT))
        screen.blit(captureImg, (0, 0))

        for box in boxes:
            draw.polygon(screen, (0, 255, 0), box, 2)

        draw.polygon(screen, (255, 0, 0), targetted_box, 2)

        display.flip()

        image.save(screen, "screenshot.jpeg")

        break

    quit()

