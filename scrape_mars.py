# importing dependencies here
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import pandas as pd


def scrape():

	mars_data = {}

	# NASA MARS NEWS ----------------------------------------------------------------------------------------------------------

	URL = "https://mars.nasa.gov/news/"
	driver = webdriver.Firefox()
	driver.get(URL)
	html = driver.page_source
	driver.implicitly_wait(20)
	driver.close()

	soup = BeautifulSoup(html, "lxml")
	latest_news = soup.find("div", class_="list_text")
	latest_news_title = latest_news.find("div", class_="content_title").text
	latest_news_teaser = latest_news.find("div", class_="article_teaser_body").text
	# ---------------------------------------------------------------------------------------------------------------------------

	# JPL Mars Space Images - FEATURED IMAGE

	IMG_URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	response = requests.get(IMG_URL)
	html = response.text
	soup = BeautifulSoup(html, "lxml")
	featured_image_url = ("https://www.jpl.nasa.gov" + soup.find("a", class_="button fancybox")["data-fancybox-href"])
	# ---------------------------------------------------------------------------------------------------------------------------

	# Mars WEATHER

	WEATHER_URL = "https://twitter.com/marswxreport?lang=en"
	response = requests.get(WEATHER_URL)
	html = response.text

	soup = BeautifulSoup(html, "html.parser")
	twitter_weather_para = soup.find(
    "p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"
	)
	for para in twitter_weather_para:
	    mars_weather = para
	    break
	# ---------------------------------------------------------------------------------------------------------------------------

	# Mars Facts

	FACTS_URL = "http://space-facts.com/mars/"
	reponse = requests.get(FACTS_URL).text
	mars_facts = pd.read_html(reponse)[0]
	mars_facts_df = pd.DataFrame(mars_facts).rename(columns={0: "Description", 1: "Value"}).set_index("Description")
	mars_facts = mars_facts_df.to_html(index=True, header=True, escape=False)
	mars_facts = mars_facts.replace("\n", "")
	# ---------------------------------------------------------------------------------------------------------------------------

	# Mars Hemispheres

	HEMISPHERE_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser = Browser("firefox")   
	browser.visit(HEMISPHERE_URL)
	html = browser.html

	soup = BeautifulSoup(html, "lxml")

	page = soup.find("div", class_="result-list")
	page_items = page.find_all("div", class_="item")

	HEMISPHERE_PARTIAL_URL = "https://astrogeology.usgs.gov"
	hemisphere_image_urls = []

	for item in page_items:

	    hemisphere_dict = {}

	    #     hemisphere_dict["title"] = item.h3.text

	    url = item.find("a")["href"]
	    browser.visit(HEMISPHERE_PARTIAL_URL + url)
	    new_html = browser.html
	    soup = BeautifulSoup(new_html, "lxml")

	    hemisphere_dict["title"] = soup.find("h2", class_="title").text
	    image = soup.find("div", class_="downloads")
	    hemisphere_dict["img_url"] = image.find("a")["href"]

	    hemisphere_image_urls.append(hemisphere_dict)
	    
	browser.quit()


	# creating a dictionary of Mars data scraped
	mars_data = {"latest_news_title": latest_news_title,
				"news_para": latest_news_teaser,
				"featured_image_url": featured_image_url,
				"mars_weather": mars_weather,
				"mars_facts": mars_facts,
				"hemisphere_img_urls": hemisphere_image_urls
	}

	return mars_data
	browser.quit()