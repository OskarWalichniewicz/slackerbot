from random_word import RandomWords
from googletrans import Translator
import cyrtranslit
from PyDictionary import PyDictionary

r = RandomWords()
dictionary = PyDictionary()
translator = Translator()

def get_word_of_the_day():
    english_word = r.get_random_word(hasDictionaryDef = "true")
    return english_word

def get_definition(word):
    english_word_def = dictionary.meaning(word)
    definitions = []
    if english_word_def is not None:
        for pair in english_word_def.items():
            definitions.append(pair[0])
            definitions.append(pair[1][0])
    return definitions

def translate_wotd(word, lang):
    translated_word = translator.translate(word, dest = lang, src = 'en').text

    if lang == 'sr':
        translated_word_lat = cyrtranslit.to_latin(word)
        return translated_word, translated_word_lat

    return translated_word

def get_synonyms(word):
    syn_list = dictionary.synonym(word)
    if syn_list is not None:
        syn_string = ""
        syn_list_len = len(syn_list) - 1
        for x in syn_list:
            syn_string += x
            if syn_list.index(x) == syn_list_len:
                syn_string += "."
            else:
                syn_string += ", "
    else:
        syn_string = None

    return syn_string

def get_antonyms(word):
    ant_list = dictionary.antonym(word)
    if ant_list is not None:
        ant_string = ""
        ant_list_len = len(ant_list) - 1
        for x in ant_list:
            ant_string += x
            if ant_list.index(x) == ant_list_len:
                ant_string += "."
            else:
                ant_string += ", "
    else:
        ant_string = None
    return ant_string