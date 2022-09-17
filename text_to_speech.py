#LingoVision
#import googletrans
#print(googletrans.LANGUAGES)

from gtts import gTTS

import os

textGazed = '' #text detected

myLang = '' #language translated to (your language)

myAudio = gTTS(text = textGazed, lang = language, slow = False)

myAudio.save("") #mp3 file

os.system("") #converted mp3 file
