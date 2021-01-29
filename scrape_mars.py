# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser

#intitialize browswer
def init_browser():

    executable_path = {'executable_path': 'C:/Users/April/anaconda3/condabin/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)
    
def scrape():
    browser = init_browser()
    dictionary = {}

    # get the url for NASA's latest news
    url ="https://mars.nasa.gov/news/"
    # open the url
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(html, 'html.parser')

    # data = soup.find_all("div", class_="article_teaser_body")
    # print(html)

    # set variables for news titles
    # NT = soup.find_all('li', class_="slide")
    # news_title = soup.find('div', class_ = "content_title").get_text()
    title = soup.find('li', class_="slide")
    news_title = title.find_all('a')[1].text

    #set variables for paragraphs
    paragraphs = soup.find('div', class_="article_teaser_body").text

    dictionary["news_title"]= news_title
    dictionary["paragraph"]= paragraphs

    # print(news_title, paragraphs)
    #close the browser
    browser.quit()

    # URL of page to be scraped
    url_fact = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_fact)
    # tables

    facts_df = tables[0]
    # facts_df

    #rename the columns
    facts_df.columns=["description", "value"]
    # facts_df

    # reset the index for the df
    facts_df.set_index("description", inplace=True)

    dictionary["facts_df"]= facts_df

    # print(facts_df)

    #initalize new browser
    browser = init_browser()
    
    # get the url and oepn it with browser
    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(h_url)

    html = browser.html

    # use beautiful soup to create soup object
    soup = BeautifulSoup(html, "html.parser")

    data = soup.find_all("div", class_="item")

    data = soup.find_all("div", class_="item")

    hemisphere_img_urls = []

    # loop through image data to find title and url info
    for d in data:
        
        title = d.find("h3").text
        
        img_url = d.a["href"]
        
        url = "https://astrogeology.usgs.gov" + img_url
        
        # use requests to get full images url 
        response = requests.get(url)
        
        # create soup object
        soup = BeautifulSoup(response.text,"html.parser")
        
        # find full image url
        new_url = soup.find("img", class_="wide-image")["src"]
        
        # create full image url
        full_url = "https://astrogeology.usgs.gov" + new_url
        
    
        #make a dict and append to the list
        hemisphere_img_urls.append({"title": title, "img_url": full_url})

    browser.quit()
    dictionary["hemisphers"] = hemisphere_img_urls
    # print(hemisphere_img_urls)
    return dictionary

