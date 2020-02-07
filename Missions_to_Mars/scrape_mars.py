# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
import time
import datetime


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
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_top = 'https://www.jpl.nasa.gov'
    browser.visit(url)
    time.sleep(3)
    browser.click_link_by_id('full_image')
    time.sleep(3)
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'lxml')

    image_div = image_soup.find_all('div', class_='fancybox-inner')
    for image in image_div:
        img_tag = image.find('img')
        print(img_tag)
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
    hemi_browser = Browser('chrome', **executable_path, headless=True)


    #GET CERBERUS IMAGE
    hemi_browser.visit(mars_hemispheres_url)
    time.sleep(3)
    hemi_browser.click_link_by_partial_text('Cerberus')
    time.sleep(3)
    #get the title
    hemi_html = hemi_browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')
    hemi_title = hemi_soup.find_all('h2', class_='title')
    cerberus_title = hemi_title[0].text
    #get the image url
    hemi_image = hemi_soup.find_all('img', class_="wide-image")
    cerberus_img_url = mars_hemispheres_url_top + hemi_image[0]['src']
    

    #GET SCHIAPARELLI IMAGE
    hemi_browser.visit(mars_hemispheres_url)
    time.sleep(3)
    hemi_browser.click_link_by_partial_text('Schiaparelli')
    time.sleep(3)
    #get the title
    hemi_html = hemi_browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')
    hemi_title = hemi_soup.find_all('h2', class_='title')
    schiap_title = hemi_title[0].text
    #get the image url
    hemi_image = hemi_soup.find_all('img', class_="wide-image")
    schiap_img_url = mars_hemispheres_url_top + hemi_image[0]['src']
    

    #GET SYRTIS IMAGE
    hemi_browser.visit(mars_hemispheres_url)
    time.sleep(3)
    hemi_browser.click_link_by_partial_text('Syrtis Major')
    time.sleep(3)
    #get the title
    hemi_html = hemi_browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')
    hemi_title = hemi_soup.find_all('h2', class_='title')
    syrtis_title = hemi_title[0].text
    #get the image url
    hemi_image = hemi_soup.find_all('img', class_="wide-image")
    syrtis_img_url = mars_hemispheres_url_top + hemi_image[0]['src']
    

    #GET VALLES IMAGE
    hemi_browser.visit(mars_hemispheres_url)
    time.sleep(3)
    hemi_browser.click_link_by_partial_text('Valles Marineris')
    time.sleep(3)
    #get the title
    hemi_html = hemi_browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')
    hemi_title = hemi_soup.find_all('h2', class_='title')
    valles_title = hemi_title[0].text
    #get the image url
    hemi_image = hemi_soup.find_all('img', class_="wide-image")
    valles_img_url = mars_hemispheres_url_top + hemi_image[0]['src']
    

    # Close the browser after scraping
    hemi_browser.quit()
    
    
    ts = datetime.datetime.now().timestamp()
    scrape_timestamp = datetime.datetime.fromtimestamp(ts).isoformat()
    
    # stuff all of the scraped data into a dictionary
    scrape_payload = {
        "scrape_timestamp": scrape_timestamp,
        "news_title": news_title,
        "news_desc": news_p,
        "featured_image_url": featured_image_url,
        "latest_weather_tweet": latest_weather_tweet,
        "mars_facts_html_table": mars_facts_html_table,
        "cerberus_title": cerberus_title,
        "cerberus_img_url": cerberus_img_url,
        "schiap_title": cerberus_title,
        "schiap_img_url": cerberus_img_url,
        "syrtis_title": cerberus_title,
        "syrtis_img_url": cerberus_img_url,
        "valles_title": cerberus_title,
        "valles_img_url": cerberus_img_url
    }

    # Store the Dictionary in MongoDB
    # Define the 'classDB' database in Mongo
    db = client.Mars_Data_DB
    db.mars_html_scrapes.insert_one(scrape_payload)
    client.close()
        
    # Return results
    return scrape_payload