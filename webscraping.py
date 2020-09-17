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
    driver.get('https://randomwordgenerator.com/') # loads page

    word = driver.find_element_by_id("result")
    return str(word.text)

"""
"""
def webscrap_google_images(query, number_of_imgs, wait_time=1):
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
def webscrap_9gag():
    chrome_options.add_argument("--user-agent=Chrome/77") # Added because webscrap_9gag doesnt work just in headless.
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    while True:
        url = 'https://9gag.com/shuffle'
        driver.get(url)
        gag_id = driver.current_url[21:] # get gag id from url
        title = driver.find_element_by_tag_name("h1").text
        link_to_gag = 'https://9gag.com/gag/{}'.format(gag_id)

        posts = driver.find_elements_by_class_name("post-container")
        for post in posts:
            all_children_by_css = post.find_elements_by_css_selector("*")

        img_link = []
        for child in all_children_by_css:
            if child.get_attribute('srcset') and 'http' in child.get_attribute('srcset') and 'webp' in child.get_attribute('srcset'): # if an image
                img_link.append(child.get_attribute('srcset'))
                return img_link[0], link_to_gag, title
            else:
                continue