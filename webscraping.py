from selenium import webdriver
import time
import os
from urllib import request as urlrequest, parse as urlparse
import json

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
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

"""
Driver opens a site and looks for element with id "result".
returns scrapped word (string)
"""
def webscrap_word():
    driver.get('https://randomwordgenerator.com/') # loads page

    word = driver.find_element_by_id("result")
    return str(word.text)

"""
"""
def webscrap_google_images(query, number_of_imgs, wait_time=1):
    # creates a webdriver with given path to chromedriver and previously set options.
    search_url = "https://www.google.com/search?tbm=isch&q={}".format(query) # tbm=isch means image

    driver.get(search_url) # loads page

    image_urls = []
    image_count = 0

    while image_count < number_of_imgs:
        thumbnail_results = driver.find_elements_by_css_selector("img.Q4LuWd") # get all image thumbnail results
        number_results = len(thumbnail_results)

        for img in thumbnail_results: # try to click every thumbnail, to show actual image
            try:
                img.click()
                time.sleep(wait_time)
            except Exception:
                continue

            actual_images = driver.find_elements_by_css_selector('img.n3VNCb') # extract previously opened image's urls
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.append(actual_image.get_attribute('src'))
            image_count = len(image_urls)

            if len(image_urls) >= number_of_imgs: # if we get amount of images we asked for while calling function
                break

    return image_urls

"""
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

def webscrap_cat():
    url = 'http://theoldreader.com/kittens/800/600/js'
    driver.get(url)
    cat = driver.find_element_by_xpath("/html/body/a/img")
    cat_img = cat.get_attribute('src')
    return cat_img

def webscrap_dog():
    load_json = json.loads(urlrequest.urlopen("https://dog.ceo/api/breeds/image/random").read().decode("utf-8"))
    return load_json['message']