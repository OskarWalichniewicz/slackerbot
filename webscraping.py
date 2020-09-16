from selenium import webdriver
import time
import os

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
    driver.get('https://randomwordgenerator.com/')

    word = driver.find_element_by_id("result")
    return str(word.text)

def webscrap_google_image(word):
    url = 'http://www.google.com/images?q={}'.format(word)
    driver.get(url)

    img_thumbnails = driver.find_element_by_css_selector("img.Q4LuWd")
    for img in img_thumbnails:
        img.click()
        time.sleep(1)
        actual_image = driver.find_elements_by_css_selector('img.n3VNCb')
        image_url = actual_image[0].get_attribute('src')
        if len(image_url) <= 2000: # discord limit
            break

    return image_url