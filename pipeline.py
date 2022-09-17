import imgToText
import LingoVisionTTS
import LingoVisionTranslator
import textBoundsUI

def pipeline(frame, coordinate, set_current_frame):
    language = 'ZH'

    print('received frame of size', len(frame), 'and coordinates:', coordinate)

    # Extract the text at the target location
    text, boxes, targeted_box = imgToText.detect_text_swagger(frame, coordinate)

    print('Boxes:', boxes, 'Targetted Box:', targeted_box)
    print('Original:', text)

    # Overlay boxes to show where OCR is being executed, along with the target frame
    boxed_frame = textBoundsUI.swaggertextBoundDebug(frame, boxes, targeted_box)

    # Freezeframe that is used for analysis
    set_current_frame(boxed_frame, coordinate)

    translated = LingoVisionTranslator.translateText(text, language)

    print('Translated:', translated)

    LingoVisionTTS.textToSpeech(translated, language)

    # Perform translation

    # Perform text to speech

    # Profit
