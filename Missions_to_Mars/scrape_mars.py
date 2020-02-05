# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
import time


def scrape_info():
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    title_results = soup.find_all('div', class_='content_title')
    news_title = title_results[0].text


    description_results = soup.find_all('div', class_='rollover_description_inner')
    news_p = description_results[0].text

    #JPL Mars Featured Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_top = 'https://www.jpl.nasa.gov'
    browser.visit(url)
    browser.click_link_by_id('full_image')
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'lxml')

    image_div = image_soup.find_all('div', class_='fancybox-inner')
    for image in image_div:
        img_tag = image.find('img')
        img_path = img_tag['src']

    featured_image_url = url_top + img_path
    browser.quit()

    ##Mars Weather Tweet
    mars_tweet_url = 'https://twitter.com/marswxreport?lang=en'
    tweet_response = requests.get(mars_tweet_url)
    # Create BeautifulSoup object; parse with 'lxml'

    tweet_soup = BeautifulSoup(tweet_response.text, 'lxml')
    tweets = tweet_soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    latest_weather_tweet = tweets[0].text


    #MARS FACTS Y'ALL!!!
    url = 'https://space-facts.com/mars/'
    mars_tables = pd.read_html(url)
    mars_facts = mars_tables[0]
    mars_facts.rename(columns ={0: 'Attribute'}, inplace = True )
    mars_facts.rename(columns ={1: 'Value'}, inplace = True )
    mars_facts_html_table = mars_facts.to_html(index=False)

    #Mars Hemisphere Images
    mars_hemispheres_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_hemispheres_url_top = 'https://astrogeology.usgs.gov'
    hemisphere_list = []
    hemi_browser = Browser('chrome', **executable_path, headless=False)


    #GET CERBERUS IMAGE
    hemi_browser.visit(mars_hemispheres_url)
    hemi_browser.click_link_by_partial_text('Cerberus')
    #get the title
    hemi_html = hemi_browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')
    hemi_title = hemi_soup.find_all('h2', class_='title')
    hemi_title_text = hemi_title[0].text
    #get the image url
    hemi_image = hemi_soup.find_all('img', class_="wide-image")
    hemi_img_url = mars_hemispheres_url_top + hemi_image[0]['src']
    # create dictionary and append to list
    hemi_dict = {"title": hemi_title_text, "img_url": hemi_img_url}
    hemisphere_list.append(hemi_dict)

    #GET SCHIAPARELLI IMAGE
    hemi_browser.visit(mars_hemispheres_url)
    hemi_browser.click_link_by_partial_text('Schiaparelli')
    #get the title
    hemi_html = hemi_browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')
    hemi_title = hemi_soup.find_all('h2', class_='title')
    hemi_title_text = hemi_title[0].text
    #get the image url
    hemi_image = hemi_soup.find_all('img', class_="wide-image")
    hemi_img_url = mars_hemispheres_url_top + hemi_image[0]['src']
    # create dictionary and append to list
    hemi_dict = {"title": hemi_title_text, "img_url": hemi_img_url}
    hemisphere_list.append(hemi_dict)

    #GET SYRTIS IMAGE
    hemi_browser.visit(mars_hemispheres_url)
    hemi_browser.click_link_by_partial_text('Syrtis Major')
    #get the title
    hemi_html = hemi_browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')
    hemi_title = hemi_soup.find_all('h2', class_='title')
    hemi_title_text = hemi_title[0].text
    #get the image url
    hemi_image = hemi_soup.find_all('img', class_="wide-image")
    hemi_img_url = mars_hemispheres_url_top + hemi_image[0]['src']
    # create dictionary and append to list
    hemi_dict = {"title": hemi_title_text, "img_url": hemi_img_url}
    hemisphere_list.append(hemi_dict)

    #GET VALLES IMAGE
    hemi_browser.visit(mars_hemispheres_url)
    hemi_browser.click_link_by_partial_text('Valles Marineris')
    #get the title
    hemi_html = hemi_browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')
    hemi_title = hemi_soup.find_all('h2', class_='title')
    hemi_title_text = hemi_title[0].text
    #get the image url
    hemi_image = hemi_soup.find_all('img', class_="wide-image")
    hemi_img_url = mars_hemispheres_url_top + hemi_image[0]['src']
    # create dictionary and append to list
    hemi_dict = {"title": hemi_title_text, "img_url": hemi_img_url}
    hemisphere_list.append(hemi_dict)

    # Close the browser after scraping
    hemi_browser.quit()

    # Return results
    