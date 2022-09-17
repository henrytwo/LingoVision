
import deepl



def translateText(untranslated, userLanguage):

    translated = ""

    auth_key = "d0ccf683-2bc8-7cef-0a12-c0496b1753fc:fx"  # Replace with your key
    translator = deepl.Translator(auth_key)

    
    result = translator.translate_text(untranslated, target_lang=userLanguage)

    translated = result.text

    return translated


print(translateText("je", "EN-US"))
