from googletrans import Translator

translator = Translator()

def translate_serbian(text):
    outp = translator.translate(text, dest = 'sr').text
    return str(outp)

def translate_english(text):
    outp = translator.translate(text, dest = 'en').text
    return str(outp)

def translate_dutch(text):
    outp = translator.translate(text, dest = 'nl').text
    return str(outp)

def translate_italian(text):
    outp = translator.translate(text, dest = 'it').text
    return str(outp)