from googletrans import Translator
import cyrtranslit
from nltk.corpus import wordnet
from webscraping import *

translator = Translator() # creates googletrans Translator object

"""
Calls webscrap_word() from webscraping and returns it.
returns str
"""
def get_random_word():
    english_word = webscrap_word()
    return english_word

"""
Gets information (definitions, synonyms, antonyms) about given word from Wordnet (http://wordnetweb.princeton.edu/perl/webwn) using nltk.
params: word (string) - a word about which information will be searched

returns 3 strings: definitions, synonyms, antonyms.
"""
def get_word_info(word):
    syns = wordnet.synsets(word) # returns list
    definitions = []
    def_string = ""

    for x in range(len(syns)):
        definitions.append(syns[x].definition()) # populates definitions (list) with definitions

    def_len = len(definitions) - 1
    for i in definitions:
        def_string += i # populates definitions (string) from list
        if not definitions.index(i) == def_len: # Check if element is last in the list; if so it ends with '.', intead of ';\n'
            def_string += ";\n"
        else:
            def_string += "."

    antonyms_list = []
    ant_string = ""
    synonyms_list = []
    syn_string = ""

    for syn in syns:
        for l in syn.lemmas(): # for every synonym
            if l.name() not in synonyms_list and l.name() != word: #if synonym doesn't already exists in list AND synonym is not the same as word.
                synonyms_list.append(l.name()) # populates synonyms (list)
            if l.antonyms(): # if word is antonym
                if l.antonyms() not in antonyms_list and l.name() != word: #if antonym doesn't already exists in list AND antonym is not the same as word.
                    antonyms_list.append(l.antonyms()[0].name()) # populates antonyms (list)

    """
    Changes antonyms_list and synonyms_list into ant_string and ant_string
    """
    ant_len = len(antonyms_list) - 1
    for i in antonyms_list:
        ant_string += i # populates antonyms (string) with antonyms from list
        if antonyms_list.index(i) == ant_len: # Check if element is last in the list; if so it ends with '.', intead of ';\n'
            ant_string += "."
        else:
            ant_string += ", "

    syn_len = len(synonyms_list) - 1
    for i in synonyms_list:
        syn_string += i # populates synonyms (string) with synonyms from list
        if synonyms_list.index(i) == syn_len: # Check if element is last in the list; if so it ends with '.', intead of ';\n'
            syn_string += "."
        else:
            syn_string += ", "

    return def_string, syn_string, ant_string

"""
Translate word to language using googletrans.
params: word (string) - word that is being translated
        lang (string) - code of language to which it should be translated.

returns translated_word (string) or
        if serbian:
            translated_word in cyrillic (string) and translated word in latin (string)
"""
def translate_word(word, lang):
    translated_word = translator.translate(word, dest = lang, src = 'en').text # src is code of language from which word is being translated (english)

    if lang == 'sr': # if translating into serbian
        translated_word_lat = cyrtranslit.to_latin(translated_word) # also adding latin version of word using cytranslit.
        return translated_word, translated_word_lat
    else:
        return translated_word