import firebase_admin
from firebase_admin import firestore
import time

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()


def add_translation(start_lang, end_lang, source_text, translated_text, source_img) :
    doc_ref = db.collection(u'settings').document(u'setting').collection(u'translation_history')
    record = {
        u'start_lang': start_lang,
        u'end_lang': end_lang,
        u'source_text': source_text,
        u'translated_text': translated_text,
        u'timestamp': time.time()
    }

    print('Updated Firebase record:', record)

    record[u'source_img'] = source_img

    doc_ref.add(record)

def get_translations() :
    settings_ref = db.collection(u'settings').document(u'setting').collection(u'translation_history')
    transactions = settings_ref.stream()

    for transaction in transactions:
        print(f'{transaction.id} => {transaction.to_dict()}')


def set_lang(lang) :
    db.collection(u'settings').document(u'setting').update({
        u'language': lang
    })

def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')

    print(doc_snapshot[0].to_dict())

if __name__ == '__main__':
    db.collection(u'settings').document(u'setting').on_snapshot(on_snapshot)
    input('press key to exit...')