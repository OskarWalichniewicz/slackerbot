from selenium import webdriver
import time
import os
from urllib import request as urlrequest, parse as urlparse
import json
import random
import wikipedia

"""
Creates options object and passes:
--headless - runs in headless mode (no UI or server dependencies)
--disable-dev-shm-usage - The /dev/shm partition is too small in certain VM environments, causing Chrome to fail or crash (see http://crbug.com/715363). Use this flag to work-around this issue (a temporary directory will always be used to create anonymous shared memory files).
--no-sandbox - Disables the sandbox for all process types that are normally sandboxed. Meant to be used as a browser-level switch for testing purposes only.
Full list: https://peter.sh/experiments/chromium-command-line-switches/

chrome_options.binary_location is a path where google chrome is located.
"""
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# creates a webdriver with given path to chromedriver and previously set options.
driver = webdriver.Chrome(executable_path=os.environ.get(
    "CHROMEDRIVER_PATH"), chrome_options=chrome_options)

"""
Opens randomwordgenerator.com site and gets the word from there.
returns scrapped word (string)
"""


def webscrap_word():
    driver.get('https://randomwordgenerator.com/')  # loads page
    word = driver.find_element_by_id("result")  # finds result
    return str(word.text)


"""
Opens Google Search (images only) and gets all the images from the first page with given query.
params: query (str) - query (word, sentence) that we want to search in google image
        number_of_imgs (int) - how many images do we want to get (maximum being images at first page of google search - next page not implemented)
        wait_time (int; default = 1) - number of seconds that driver waits before it starts scrapping (needed for site to loads)
returns scrapped images (list)
"""


def webscrap_google_images(query, number_of_imgs, wait_time=1):
    # creates a webdriver with given path to chromedriver and previously set options.
    # tbm=isch means image
    search_url = "https://www.google.com/search?tbm=isch&q={}".format(query)
    driver.get(search_url)  # loads page
    image_urls = []
    image_count = 0
    while image_count < number_of_imgs:  # as long as list is not populated
        thumbnail_results = driver.find_elements_by_css_selector(
            "img.Q4LuWd")  # get all image thumbnail results

        for img in thumbnail_results:  # try to click every thumbnail, to show actual image
            try:
                img.click()
                time.sleep(wait_time)
            except Exception:
                continue

            actual_images = driver.find_elements_by_css_selector(
                'img.n3VNCb')  # extract previously opened image's urls
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.append(actual_image.get_attribute('src'))
            image_count = len(image_urls)

            # if we get amount of images we asked for while calling function
            if len(image_urls) >= number_of_imgs:
                break

    return image_urls


"""
Opens mentalfloss.com/amazingfactgenerator and gets facts from there (text and image).
returns image url (string), fact description (string)
"""


def webscrap_fact():
    while True:
        url = 'https://www.mentalfloss.com/amazingfactgenerator'
        driver.get(url)
        time.sleep(2)
        desc = driver.find_element_by_class_name("af-details")
        img_url = desc.get_attribute("data-img-src")
        fact_descr = desc.get_attribute("data-description")
        return img_url, fact_descr


"""
Using some-random-api (some-random-api.ml) and gets image from there.
params: thing (string) - query, thing of which we want to get picture. List at (https://docs.some-random-api.ml/json/image)
returns image url (string)
"""


def webscrap_random_api(thing):
    url = 'https://some-random-api.ml/img/{}'.format(thing)
    # doesnt work without it (404 not found request)
    req = urlrequest.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    load_json = json.loads(urlrequest.urlopen(req).read())
    return load_json['link']


"""
Using some-random-api (some-random-api.ml) and gets fact from there.
params: thing (string) - query, thing of which we want to get fact. List at (https://docs.some-random-api.ml/json/facts)
returns fact (string)
"""


def webscrap_random_api_fact(thing):
    url = 'https://some-random-api.ml/facts/{}'.format(thing)
    # doesnt work without it (404 not found request)
    req = urlrequest.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    load_json = json.loads(urlrequest.urlopen(req).read())
    return load_json['fact']


"""
Using random-d.uk API (https://random-d.uk/api) and gets duck picture from there.
returns image url (string)
"""


def webscrap_duck():
    url = 'https://random-d.uk/api/v2/random'
    req = urlrequest.Request(url)
    load_json = json.loads(urlrequest.urlopen(req).read())
    return load_json['url']


"""
Using dog.ceo API (https://dog.ceo/dog-api/) and gets dog picture from there.
returns image url (string)
"""


def webscrap_dog():
    load_json = json.loads(urlrequest.urlopen(
        "https://dog.ceo/api/breeds/image/random").read().decode("utf-8"))
    return load_json['message']


"""
Uses google didyoumean feature from google translate.
params: origin language (auto or en)
        destination language - can be anything
        query - if spaces, replace them with +
returns didyoumean text or
        empty string (if didyoumean was not found)
"""


def webscrap_didyoumean(query, origin_language='auto', destination_language='en'):
    url = 'http://translate.google.com/#{}|{}|{}'.format(
        origin_language, destination_language, query)
    driver.get(url)
    time.sleep(1)
    try:
        didyoumean = driver.find_element_by_id("spelling-correction")
        didyoumean_text = didyoumean.text
        if "Showing translation for" in didyoumean_text:
            separator = 'for'
            first_line = didyoumean_text.split("\n")[0]
            didyoumean_final = first_line.split(separator, 1)[1][1:]
        elif "Did you mean:" in didyoumean_text:
            separator = ':'
            # seperate text with : (cuz its "Did you mean: [word]") and also removes first character (space)
            first_line = didyoumean_text.split("\n")[0]
            didyoumean_final = first_line.split(separator, 1)[1][1:]
        else:
            didyoumean_final = ""
        return didyoumean_final
    except IndexError:
        return ""


"""
"""


def webscrap_trivia():
    load_json = json.loads(urlrequest.urlopen(
        "https://opentdb.com/api.php?amount=1").read().decode("utf-8"))

    results = load_json['results'][0]

    correct_answer = []
    correct_answer.append(results['correct_answer'])

    # answers = results['incorrect_answers'] + results['correct_answer']
    answers = results['incorrect_answers'] + correct_answer
    random.shuffle(answers)

    category = results['category']
    difficulty = results['difficulty']
    question = results['question']
    typ = results['type']
    correct_answer_str = correct_answer[0]

    return category, difficulty, question, correct_answer_str, answers, typ


"""
https://github.com/15Dkatz/official_joke_api
"""


def webscrap_joke():
    url = 'https://official-joke-api.appspot.com/random_joke'
    load_json = json.loads(urlrequest.urlopen(url).read())
    joke = str(load_json['setup']) + "\n.\n.\n.\n" + \
        str(load_json['punchline'])
    return joke


"""
https://api.adviceslip.com/
"""


def webscrap_advice():
    url = 'https://api.adviceslip.com/advice'
    load_json = json.loads(urlrequest.urlopen(url).read())
    return load_json['slip']['advice']


"""
"""


def webscrap_insult():
    url = 'https://evilinsult.com/generate_insult.php?lang=en&type=json'
    load_json = json.loads(urlrequest.urlopen(url).read())
    return load_json['insult']


"""
"""


def webscrap_horoscope(sign):
    url = 'https://www.astrology.com/horoscope/daily/{}.html'.format(sign)
    driver.get(url)
    try:
        horoscope = driver.find_element_by_xpath(
            "/html/body/section/section/div[2]/main/p[1]")
        horoscope_text = horoscope.text

        date = horoscope_text.split(":")[0]
        if date in horoscope_text:
            horoscope_text = horoscope_text.replace(date, '')

        return horoscope_text[2:]  # removes date and whitespace
    except:
        return ""


"""
"""


def webscrap_wikipedia(article='random'):
    wikipedia.set_lang('en')
    if article == 'random':
        title = wikipedia.random()

        try:
            article = wikipedia.page(title)
        except wikipedia.DisambiguationError as e:
            article = wikipedia.page(e.options[0])

        article_url = article.url
        summary = article.summary

        return article_url, title, summary

    else:
        title = article
        options = None
        try:
            article = wikipedia.page(title)
            article_url = article.url
            summary = article.summary
        except wikipedia.DisambiguationError as e:
            number_of_options = len(e.options)
            if number_of_options > 5:
                number_of_options = 5
            options = e.options[:number_of_options]
        except KeyError:
            title = title.replace("(", "")
            article = wikipedia.page(title)
            article_url = article.url
            summary = article.summary

        if options is None:
            return article_url, title, summary
        else:
            return options
