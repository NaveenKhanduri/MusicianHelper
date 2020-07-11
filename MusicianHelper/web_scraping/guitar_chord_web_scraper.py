from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxProfile
from selenium import webdriver


def init_browser():

    fp = FirefoxProfile("//home/shetdedoe/.mozilla/firefox/ixj5l1k6.MusicianProfile/")
    options = webdriver.FirefoxOptions()
    options.set_headless()
    browser = Firefox(firefox_profile=fp, firefox_options=options)
    return browser


#returns a tuple consisting of links to guitar chord pages, and a list of every link on the page. Second tuple element is just for debugging purposes
def link_list(browser):
    #link to page on ultimate-guitar.com which contains links to guitar chord pages
    # html.parser has almost the same speed as xlm, and is almost as accurate as html5lib, so its a good middle ground
    html = browser.page_source
    soup_parsed = BeautifulSoup(html, 'html.parser')

    body = soup_parsed.find("body").find('main').find_all('article')
    raw_links = body[2].find_all('a')
    ###########    This will most likely need to be regularly updated. It is a list of key words that links to chords do not have
    bad_words = ["explore?type[]", 'artist']
    ###############

    good_links = [link.attrs['href'] for link in raw_links if not any(bw in link.attrs['href'] for bw in bad_words)]
    try:
        key = body[1].find_all('a')[1].text
        return key, good_links
    except:
        print("Could not find keys")
        return 0, good_links


#implicitly assumes firefox geko is in the same directory as the function. Returns a Browser object

#should return a tuple consisting of the artist, the song name, and the chords
def chord_scraper(browser):

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    body = soup.find('body').find('main').find('pre')
    chords = [c.text for c in body.find_all(attrs={'data-name': True})]

    header = soup.find('body').find('main').find_all('header')

    artists = header[1].find_all("a")
    if len(artists) > 1:
        artist = ""
        for a in artists:
            artist = artist + "/" + a.text
    else:
        artist = artists[0].text

    title = header[1].find('h1').text

    return title, artist, chords


