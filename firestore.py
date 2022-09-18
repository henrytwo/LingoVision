import firebase_admin
from firebase_admin import firestore

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()


def add_translation(start_lang, end_lang, source_text, translated_text, source_img) :
    doc_ref = db.collection(u'settings').document(u'setting').collection(u'translation-history')
    doc_ref.add({
        u'start_lang': start_lang,
        u'end-lang': end_lang,
        u'source-text': source_text,
        u'translated-text': translated_text,
        u'source-img': source_img
    })


def get_translations() :
    settings_ref = db.collection(u'settings').document(u'setting').collection(u'translation-history')
    transactions = settings_ref.stream()

    for transaction in transactions:
        print(f'{transaction.id} => {transaction.to_dict()}')


def change_lang(lang) :
    doc_ref = db.collection(u'settings').document(u'setting').update({
        u'language': lang
    })



def on_snapshot(doc_snapshot):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')
    
    print(doc_snapshot.data())


db.collection(u'settings').document(u'setting').on_snapshot(on_snapshot)