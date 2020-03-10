import pandas as pd
import matplotlib as plt
from bs4 import BeautifulSoup as bs
import requests
import splinter as sp
from splinter import Browser
from bs4 import BeautifulSoup
import os
import time
import datetime as dt

#Site Navigation
executable_path = {"executable_path": "/usr/local/Caskroom/chromedriver/80.0.3987.106/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

class scrapebot():

    def getsoup(url,sleep):
        browser.visit(url)
        time.sleep(int(sleep))
        html=browser.html
        soup = bs(html, "html.parser")
        return soup

    def nasamarsnews():
        nasa_url = "https://mars.nasa.gov/news/"
        soup = scrapebot.getsoup(nasa_url,"10")
        ntitle=""
        ncontent=""
        try:
            ntitle=soup.find('div', class_='content_title').text
            ncontent=soup.find('div', class_='article_teaser_body').text
            # Optional for getting all the Titles
            news_title=[]
            TitlesCollection = soup.find_all("div", class_='list_text')
            for T in TitlesCollection:
                SepDIV=T.find_all('div', class_='content_title')
                for S in SepDIV:
                    news_title.append(S.a.text)

            # Optional for getting all the Content
            news_p=[]
            ContentCollection = soup.find_all("div", class_='article_teaser_body')
            for T in TitlesCollection:
                SepDIV=T.find_all("div", class_='article_teaser_body')
                for S in SepDIV:
                    news_p.append(S.text)
            output=[news_title,news_p]
        except NameError:
            print(NameError)
        return ntitle,ncontent

    def marsimage():
        MarsImageURL="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        # browser.visit(MarsImageURL)
        # Mhtml=browser.html
        # msoup=bs(Mhtml, 'lxml')
        msoup = scrapebot.getsoup(MarsImageURL,"1")
        ImageURL = msoup.find("img", class_="thumb")["src"]
        featured_image_url = "https://www.jpl.nasa.gov" + ImageURL
        return featured_image_url

    def twitter():
        twitter = 'https://twitter.com/marswxreport?lang=en'
        # browser.visit(twitter)
        # time.sleep(1)
        # twitterHTML = browser.html

        # tsoup = bs(twitterHTML, 'html.parser')
        tsoup = scrapebot.getsoup(twitter,"5")
        # Find all elements in span
        allspan = tsoup.body.find_all('span')

        mars_weather=""
        for tweet in allspan:
            #print(tweet.text)
            mars_weather_tweet = tweet.text
            if 'sol' and 'pressure' in mars_weather_tweet:
                mars_weather=mars_weather_tweet
                return mars_weather
                break
            else:
                pass
        return mars_weather

    def marsfacts():
        marsfacts="https://space-facts.com/mars"
        browser.visit(marsfacts)
        tables=pd.read_html(marsfacts)
        mars_data = pd.DataFrame(tables[0])
        mars_facts = mars_data.to_html(header = False, index = False)
        return mars_facts

    def marshemisphere():
        marsimage="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        # browser.visit(marsimage)
        #
        #
        # html = browser.html
        # mhsoup = bs(html, "html.parser")
        mhsoup = scrapebot.getsoup(marsimage,"1")
        hemisphere_image_urls = []

        result = mhsoup.find("div", class_ = "result-list" )
        hemispheres = result.find_all("div", class_="item")


        for h in hemispheres:
            title= h.h3.text.replace("Enhanced","")
            subpage="https://astrogeology.usgs.gov" + h.a["href"]
            browser.visit(subpage)
            time.sleep(2)
            subhtml=browser.html
            subsoup=bs(subhtml,"html5lib")
            getdownloads=subsoup.find('div',class_='downloads')
            #print(getdownloads)
            fullimage=getdownloads.find("a")["href"]
            hemisphere_image_urls.append({"title":title,"img_url":fullimage})
        return hemisphere_image_urls

    def scrape():
        mars_news=scrapebot.nasamarsnews()
        all_data = {
            'news_title' :  mars_news[0],
            'news_p' :  mars_news[1],
            'featured_image_url' : scrapebot.marsimage(),
            'mars_weather' : scrapebot.twitter(),
            'mars_facts' : scrapebot.marsfacts(),
            'hemisphere_image_urls' : scrapebot.marshemisphere(),
            'timestamp' : dt.datetime.now()
            }
        browser.quit()
        print(all_data)
        return all_data
