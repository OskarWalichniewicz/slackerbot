from googletrans import Translator

translator = Translator()

def translate_serbian(text):
    outp = translator.translate(text, dest = 'sr').text
    return str(outp)

def translate_english(text):
    outp = translator.translate(text, dest = 'en').text
    return str(outp)