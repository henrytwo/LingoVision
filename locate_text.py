import cv2
import numpy as np

def locate_text(frame, coordinate):
    nparr = np.fromstring(frame, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1

    print(img_np.shape)