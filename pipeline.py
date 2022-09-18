import imgToText
import LingoVisionTTS
import LingoVisionTranslator
import textBoundsUI
import threading
import playAudio
import time

currently_running = False

def pipeline(frame, coordinate, set_current_frame):
    def runner():
        global currently_running

        currently_running = True

        language = 'ZH' #'EN-US'

        set_current_frame(frame, coordinate)

        playAudio.startSound()

        print('received frame of size', len(frame), 'and coordinates:', coordinate)

        # Extract the text at the target location
        text, boxes, targeted_box = imgToText.detect_text_swagger(frame, coordinate)

        print('Boxes:', boxes, 'Targetted Box:', targeted_box)
        print('Original:', text)

        with open('frame.jpg', 'wb') as file:
            file.write(frame)

        # Overlay boxes to show where OCR is being executed, along with the target frame
        textBoundsUI.textBoundDebug('frame.jpg', boxes, targeted_box)

        with open('screenshot.jpeg', 'rb') as file:
            boxed_frame = file.read()

        # Freezeframe that is used for analysis
        set_current_frame(boxed_frame, coordinate)

        if not text:
            playAudio.errorSound()
            time.sleep(0.5)
            print('No text detected')
            text = 'No text detected!'

        translated = LingoVisionTranslator.translateText(text, language)

        print('Translated:', translated)

        LingoVisionTTS.textToSpeech(translated, language)

        currently_running = False

    if not currently_running:
        thread = threading.Thread(target=runner)
        thread.start()
    else:
        print('Already running - skipping command')
