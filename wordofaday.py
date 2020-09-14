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
    translated_word = translator.translate(word, dest = lang, src = 'en')

    if lang == 'sr':
        translated_word_lat = cyrtranslit.to_latin(word)
        return translated_word, translated_word_lat

    return translated_word