from random_word import RandomWords
from googletrans import Translator
import cyrtranslit

r = RandomWords()
translator = Translator()

def get_word_of_the_day():
    english_word = r.get_random_word()

    serbian_word_cyr = translator.translate(english_word, dest = 'sr').text
    serbian_word_lat = cyrtranslit.to_latin(serbian_word_cyr)
    serbian_word = serbian_word_cyr + " / " + serbian_word_lat

    italian_word = translator.translate(english_word, dest = 'it').text

    dutch_word = translator.translate(english_word, dest = 'nl').text

    polish_word = translator.translate(english_word, dest = 'pl').text

    romanian_word = translator.translate(english_word, dest = 'ro').text

    return english_word, serbian_word, italian_word, dutch_word, polish_word, romanian_word