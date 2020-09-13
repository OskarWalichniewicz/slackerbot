from googletrans import Translator

translator = Translator()

def translate_serbian(text):
    return str(translator.translate(text, dest = 'sr').text)

def translate_english(text):
    return str(translator.translate(text, dest = 'en').text)