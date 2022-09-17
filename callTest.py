
from imgToText import detect_text
from textBoundsUI import textBoundDebug

textInfo = detect_text("imgs\\raw_capture.png")

textBoundDebug("./imgs/raw_capture.png", textInfo[1], textInfo[2])

print(textInfo[0])

