from random_word import RandomWords
from googletrans import Translator
import cyrtranslit

r = RandomWords()
translator = Translator()

def get_word_of_the_day():
    english_word = r.get_random_word(hasDictionaryDef = "true")

    serbian_word_cyr = translator.translate(english_word, dest = 'sr', src='en').text
    serbian_word_lat = cyrtranslit.to_latin(serbian_word_cyr)
    serbian_word = serbian_word_cyr + " / " + serbian_word_lat

    italian_word = translator.translate(english_word, dest = 'it', src='en').text

    dutch_word = translator.translate(english_word, dest = 'nl', src='en').text

    polish_word = translator.translate(english_word, dest = 'pl', src='en').text

    romanian_word = translator.translate(english_word, dest = 'ro', src='en').text

    return english_word, serbian_word, italian_word, dutch_word, polish_word, romanian_word