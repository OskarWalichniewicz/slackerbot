from googletrans import Translator
import cyrtranslit

translator = Translator()

def translate_serbian(text):
    outp_cyr = translator.translate(text, dest = 'sr').text
    outp_lat = cyrtranslit.to_latin(outp_cyr)
    return str(outp_cyr + "\n" + outp_lat)

def translate_english(text):
    outp = translator.translate(text, dest = 'en').text
    return str(outp)

def translate_dutch(text):
    outp = translator.translate(text, dest = 'nl').text
    return str(outp)

def translate_italian(text):
    outp = translator.translate(text, dest = 'it').text
    return str(outp)

def translate_polish(text):
    outp = translator.translate(text, dest = 'pl').text
    return str(outp)