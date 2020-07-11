from web_scraping.guitar_chord_web_scraper import *
import pickle
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from pymongo import MongoClient

temp_data = {}
base_link = "https://www.ultimate-guitar.com/explore?type[]=Official&&tonality[]="

browser = init_browser()

keynums = [i for i in range(2, 31)]
temp_data = {}


def timer(driver):
    limit = 0
    pathname = "//code//span"
    while limit < 30:
        if len(driver.find_elements_by_xpath(pathname)) < 2:
            limit += 1
            time.sleep(0.25)
        else:
            return True
    raise ValueError("taking too dang long")

#finds top songs for every key, and returns a dictionary of key with a list of links to chord pages
for key in keynums:
    main_page = f'{base_link}{key}'
    browser.get(main_page)
    key_links = link_list(browser)
    print(key)
    try:
        song_list = {}
        for link in key_links[1]:
            # have to wait until page loads javascript data before it can be navigated properly
            css_path = "#canvas > canvas:nth-child(2)"
            browser.get(link)
            wait = WebDriverWait(browser, 30)
            element = wait.until(expected_conditions.visibility_of(browser.find_element_by_css_selector(css_path)))
            time.sleep(0.5)
            button = browser.find_element_by_xpath("//div[contains(text(),'Chords')]")
            button.click()
            timer(browser)

            chord_tuple = chord_scraper(browser)

            title = f'{chord_tuple[0]} by {chord_tuple[1]}'
            print(title)

            elem = {
                "key": key_links[0],
                "url": key_links[1],
                "title": chord_tuple[0],
                "artist": chord_tuple[1],
                "chords": chord_tuple[2]
            }

            song_list[title] = chord_tuple[2]
        temp_data[key_links[0]] = song_list
    except:
        temp_data["blank"] = key_links[1]

browser.quit()

data_file = open(os.getcwd() + '/chord_db/chord_data.pkl', 'wb')
pickle.dump(temp_data, data_file)
data_file.close()
