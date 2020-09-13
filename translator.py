from googletrans import Translator

translator = Translator()

def translate_serbian(text):
    outp = translator.translate(text, dest = 'sr').text + " / " + translator.translate(text, dest = 'sr-Latn')
    return str(outp)

def translate_english(text):
    return str(translator.translate(text, dest = 'en').text)