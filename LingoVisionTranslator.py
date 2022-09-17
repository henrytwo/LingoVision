
import deepl



def translateText(untranslated, userLanguage):

    with open('TranslatorKey.txt') as f:
        key = f.readlines()

    key = key[0]
    print(key)
    translated = ""

    auth_key = key  # Replace with your key
    translator = deepl.Translator(auth_key)

    
    result = translator.translate_text(untranslated, target_lang=userLanguage)

    translated = result.text

    return translated


print(translateText("bonjour, jemappelle john", "EN-US"))
