#LingoVision


from gtts import gTTS

import os

langGazed = '' #language detected

myLang = '' #language translated to (your language)

myAudio = gTTS(text = langGazed, lang = language, slow = False)

myAudio.save("") #mp3 file

os.system("") #converted mp3 file
