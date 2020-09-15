from googletrans import Translator
import cyrtranslit
from nltk.corpus import wordnet
from webscraping import *

translator = Translator()

def get_random_word():
    english_word = webscrap_word()
    return english_word

def get_word_info(word):
    syns = wordnet.synsets(word)
    definitions = []
    def_string = ""

    for x in range(len(syns)):
        definitions.append(syns[x].definition())

    def_len = len(definitions) - 1
    for i in definitions:
        def_string += i
        if not definitions.index(i) == def_len:
            def_string += "\n"

    antonyms_list = []
    ant_string = ""
    synonyms_list = []
    syn_string = ""

    for syn in syns:
        for l in syn.lemmas():
            if l.name() not in synonyms_list:
                synonyms_list.append(l.name())
            if l.antonyms():
                if l.antonyms() not in antonyms_list:
                    antonyms_list.append(l.antonyms()[0].name())

    ant_len = len(antonyms_list) - 1
    for i in antonyms_list:
        ant_string += i
        if antonyms_list.index(i) == ant_len:
            ant_string += "."
        else:
            ant_string += ", "

    syn_len = len(synonyms_list) - 1
    for i in synonyms_list:
        syn_string += i
        if synonyms_list.index(i) == syn_len:
            syn_string += "."
        else:
            syn_string += ", "
    return def_string, syn_string, ant_string

def translate_word(word, lang):
    translated_word = translator.translate(word, dest = lang, src = 'en').text

    if lang == 'sr':
        translated_word_lat = cyrtranslit.to_latin(translated_word)
        return translated_word, translated_word_lat
    else:
        return translated_word