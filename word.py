from googletrans import Translator
import cyrtranslit
from webscraping import *
from wordnik import *

apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.environ.get("WORDNIK_API_KEY")
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

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
def get_definitions(word):
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

def get_synonyms(word):
    syn_string = ""

    rel_word = wordApi.getRelatedWords(word, relationshipTypes = "synonym", limitPerRelationshipType = 100)
    for word in rel_word:
        syn_list = word.words

    syn_len = len(syn_list) - 1
    for syn in syn_list:
        syn_string += syn
        if not syn_list.index(syn) == syn_len: # Check if element is last in the list; if so it ends with '.', intead of ';\n'
            syn_string += ", "
        else:
            syn_string += "."

    return syn_string

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