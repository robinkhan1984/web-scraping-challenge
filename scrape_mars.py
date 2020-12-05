import pandas as pd
from bs4 import BeautifulSoup
import requests
import html
import time
import pymongo
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    results = soup.find('div', class_='list_text').a.text
    results
    results2 = soup.find('div', class_='article_teaser_body').text

    mars_data = {
    'Title' : results, 
    'Paragraph' : results2,
    }

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.find_by_id("full_image").click()

    time.sleep(2)

    browser.find_link_by_partial_text("more info").click()

    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    picture = soup.find('figure', class_='lede').a.img["src"]
    picture

    featured_image = 'https://www.jpl.nasa.gov' + picture
    featured_image

    mars_data["featured_image"] = featured_image

    url = 'https://space-facts.com/mars/'

    facts = pd.read_html(url)

    facts_cleaned = facts[1]

    facts_cleaned.columns = ["Description" , "Mars", "Earth"]

    facts_cleaned

    mars_table = facts_cleaned.to_html()

    mars_table

    mars_data["Facts"] = mars_table

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemispheres = []

    for i in range(4):
        
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[i].click()
        
        soup = BeautifulSoup(browser.html, 'html.parser')
        
        title = soup.find("h2", class_='title').get_text()
        
        img = soup.find("a", text = "Sample").get("href")
        
        hemisphere["title"] = title
        
        hemisphere["img_url"] = img
        
        hemispheres.append(hemisphere)
        
        browser.back()
        
    hemispheres

    mars_data["Hemispheres"] = hemispheres

    browser.quit()

    return mars_data