from googletrans import Translator
import cyrtranslit
from nltk.corpus import wordnet
from webscraping import *
from wordnik import *

translator = Translator() # creates googletrans Translator object

apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.environ.get("WORDNIK_API_KEY")
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

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
def get_definition(word):
    def_word = wordApi.getDefinitions(word, sourceDictionaries = 'wiktionary')
    definitions = {}

    for definition in def_word:
        def_text = definition.text
        if def_text is not None:
            try:
                def_text = def_text.replace('<xref>', '')
                def_text = def_text.replace('</xref>', '')
            except:
                pass

            def_part_of_speech = definition.partOfSpeech
            if def_part_of_speech == 'adjective':
                def_part_of_speech = 'adj'

            definitions.update({def_text: def_part_of_speech})

    str_def = ""
    for key in definitions:
        str_def += definitions[key] + ": " + key + "\n"

    return str_def

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