from googletrans import Translator
import cyrtranslit
from webscraping import *
from wordnik import *

"""
Initiates Wordnik API
"""
apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.environ.get("WORDNIK_API_KEY")
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

"""
Creates googletrans Translator object
"""
translator = Translator()

"""
Calls webscrap_word() from webscraping and returns it.
returns str
"""


def get_random_word():
    english_word = webscrap_word()
    return english_word


"""
Gets definition about given word from wiktionary using wordnikAPI (https://developer.wordnik.com/).
params: word (string) - a word about which defition will be searched
returns definition (string)
"""


def get_definitions(word):
    def_word = wordApi.getDefinitions(word, sourceDictionaries='wiktionary')
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

            def_part_of_speech = ''.join(('*', def_part_of_speech, '*'))
            definitions.update({def_text: def_part_of_speech})

    str_def = ""
    def_len = len(definitions) - 1
    last_element_of_dict = list(definitions.keys())[-1]
    for key in definitions:
        str_def += definitions[key] + " " + key
        if not key == last_element_of_dict:
            str_def += "\n"

    return str_def


"""
Gets synonyms about given word from wordnik using wordnikAPI (https://developer.wordnik.com/).
params: word (string) - a word of which synonyms will be searched
returns synonyms (string)
"""


def get_synonyms(word):
    syn_string = ""

    rel_word = wordApi.getRelatedWords(
        word, relationshipTypes="synonym", limitPerRelationshipType=100)
    for word in rel_word:
        syn_list = word.words

    syn_len = len(syn_list) - 1
    for syn in syn_list:
        syn_string += syn
        # Check if element is last in the list; if so it ends with '.', intead of ';\n'
        if not syn_list.index(syn) == syn_len:
            syn_string += ", "
        else:
            syn_string += "."

    return syn_string


"""
Translate word to language using googletrans.
params: word (string) - word that is being translated
        lang (string) - code of language to which it should be translated.

returns translated_word (string) or
        if serbian (lang == 'sr'):
            translated_word in cyrillic (string) and translated word in latin (string)
"""


def translate_word(word, lang, src='en'):
    if src == 'auto':
        translated_word = translator.translate(word, dest=lang).text
    # src is code of language from which word is being translated (english)
    else:
        translated_word = translator.translate(word, dest=lang, src='en').text

    if lang == 'sr':  # if translating into serbian
        # also adding latin version of word using cytranslit.
        translated_word_lat = cyrtranslit.to_latin(translated_word)
        return translated_word, translated_word_lat
    else:
        return translated_word
