import imgToText
import LingoVisionTTS
import LingoVisionTranslator
import textBoundsUI
import threading
import playAudio
import time
import firestore_stuff
from firebase_admin import firestore

currently_running = False
language = 'EN-US'


def on_snapshot(doc_snapshot, changes, read_time):
    global language

    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')

    settings = doc_snapshot[0].to_dict()

    language = settings['language']

    print('Updated settings:', settings)

db = firestore.client()
db.collection(u'settings').document(u'setting').on_snapshot(on_snapshot)


def pipeline(frame, coordinate, set_current_frame):
    def runner():
        global currently_running

        currently_running = True

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

        translated, source_language = LingoVisionTranslator.translateText(text, language)

        print('Translated:', translated)

        # Update databse
        firestore_stuff.add_translation(
            start_lang=source_language,
            end_lang=language,
            source_text=text,
            translated_text=translated,
            source_img=boxed_frame
        )

        LingoVisionTTS.textToSpeech(translated, language)

        currently_running = False

    if not currently_running:
        thread = threading.Thread(target=runner)
        thread.start()
    else:
        print('Already running - skipping command')
