from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape_all():
    browser = init_browser()
    time.sleep(1)

    news_title, news_p = mars_news(browser)

    data = {"news_title":news_title,
        "news_p":news_p,
        "featured_image":featured_image(browser),
        "mars_facts":facts_html_table(),
        # "mars_hems":hemisphere_image_urls(browser)
        }
    browser.quit()
    return data

def mars_news(browser):
        
    #url of nasa mars news page to be scraped
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #retrieve page with splinter
    browser.visit(news_url)

    #create beautiful soup object
    news_soup=bs(browser.html, 'lxml')

    #scrape the latest news title
    mars_news = news_soup.find('div', class_='list_text')
    news_title = mars_news.find('div', class_='content_title').text
    print(news_title)   

    #scrape the paragraph text
    news_p = news_soup.find('div', class_='article_teaser_body').text
    print(news_p)
    # Close the browser after scraping
    # browser.quit()

    # Return results
    return news_title, news_p

def featured_image(browser):

    #urls for mars space images
    jpl_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #retrieve page with splinter
    browser.visit(image_url)

    #create beautiful soup object
    img_soup=bs(browser.html, 'lxml')

    #pull the featured image url from the carousel item button
    image = img_soup.find('a', class_="button fancybox")["data-fancybox-href"]

    #create featured url image link
    featured_image_url = jpl_url + image
    print(featured_image_url)

    # browser.quit()

    return featured_image_url

def facts_html_table():

    #save the url for the mars facts table into a variable
    facts_url = 'https://space-facts.com/mars/'

    #read only the table information from the webpage
    table = pd.read_html(facts_url)[0]
    
    #rename the columns
    facts_df = table.rename(columns={0: "Description", 1: "Mars"})

    #set the index to description
    facts_df.set_index("Description")

    return facts_df.to_html(classes="table table-striped")

def hemisphere_image_urls(browser):














