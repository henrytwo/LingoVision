from pygame import *

init()

def textBoundDebug(img, boxes, targetted_box):
    captureImg = image.load(img)

    screen = display.set_mode([captureImg.get_width(), captureImg.get_height()])
    running = True

    #exp = 5

    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        screen.blit(captureImg, (0, 0))

        for box in boxes:
            if box:
                draw.polygon(screen, (0, 255, 0), box, 2)
            #draw.polygon(screen, (0, 0, 255), [[box[0][0]-exp, box[0][1]-exp], [box[1][0]+exp, box[1][1]-exp], [box[2][0]+exp, box[2][1]+exp], [box[3][0]-exp, box[3][1]+exp]], 2)

        if targetted_box:
            draw.polygon(screen, (255, 0, 0), targetted_box, 2)

        display.flip()

        image.save(screen, "screenshot.jpeg")

        break

    quit()

