import imgToText
import LingoVisionTTS
import LingoVisionTranslator

def pipeline(frame, coordinate):
    language = 'ZH'

    print('received frame of size', len(frame), 'and coordinates:', coordinate)

    # Extract the text at the target location
    text = imgToText.detect_text_swagger(frame)

    print('Original:', text)

    translated = LingoVisionTranslator.translateText(text, language)

    print('Translated:', translated)

    LingoVisionTTS.textToSpeech(translated, language)

    # Perform translation

    # Perform text to speech

    # Profit
