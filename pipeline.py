import imgToText
import LingoVisionTTS
import LingoVisionTranslator
import textBoundsUI
import threading


def pipeline(frame, coordinate, set_current_frame):
    def runner():
        language = 'ZH'

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

        translated = LingoVisionTranslator.translateText(text, language)

        print('Translated:', translated)

        LingoVisionTTS.textToSpeech(translated, language)

    thread = threading.Thread(target=runner)
    thread.start()
