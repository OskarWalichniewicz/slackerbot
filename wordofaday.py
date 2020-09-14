from googletrans import Translator
import cyrtranslit
from nltk.corpus import wordnet
from webscraping import *

translator = Translator()

def get_word_of_the_day():
    english_word = get_random_word()
    return english_word

def get_definition(word):
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

    return def_string

def translate_wotd(word, lang):
    translated_word = translator.translate(word, dest = lang, src = 'en').text

    if lang == 'sr':
        translated_word_lat = cyrtranslit.to_latin(translated_word)
        return translated_word, translated_word_lat

    return translated_word

def get_syns_ants(word):
    syns = wordnet.synsets(word)
    antonyms = []
    ant_string = ""
    synonyms = []
    syn_string = ""

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l not in synonyms:
                synonyms.append(l.name())
            if l.antonyms():
                if l not in antonyms:
                    antonyms.append(l.antonyms()[0].name())

    ant_len = len(antonyms) - 1
    for i in antonyms:
        ant_string += i
        if not antonyms.index(i) == ant_len:
            ant_string += "."
        ant_string += ", "

    syn_len = len(synonyms) - 1
    for i in synonyms:
        syn_string += i
        if not syn.index(i) == syn_len:
            syn_string += "."
        syn_string += ", "

    return syn_string, ant_string