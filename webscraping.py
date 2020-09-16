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


def webscrap_google_images(query, max_links_to_fetch, sleep_between_interactions=1):
    def scroll_to_end():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    driver.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end()

        # get all image thumbnail results
        thumbnail_results = driver.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                break
        else:
            time.sleep(30)
            return
            load_more_button = driver.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                driver.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls