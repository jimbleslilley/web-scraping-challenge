import pandas as pd
from bs4 import BeautifulSoup as soup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    ###############################
    # Nasa Mars News Site
    ###############################

    browser = Browser('chrome', executable_path=ChromeDriverManager().install(), headless=False)

    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    news_soup = soup(html, "html.parser")
    # get the news title
    title = news_soup.select_one("div.list_text").find("div", class_="content_title").get_text()

    # get the paragraph
    paragraph = news_soup.select_one("div.list_text").find("div", class_="article_teaser_body").get_text()

    ###############################
    # JPL Mars space images
    ###############################

    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    bsobject = soup(browser.html, "html.parser")

    image = bsobject.find("img", class_="headerimage fade-in")["src"]
    image_url = url + image
    image_url

    ###############################
    # Mars Facts
    ###############################

    url = 'https://galaxyfacts-mars.com/'

    mars_df = pd.read_html("https://galaxyfacts-mars.com")[0]
        # rename columns
    mars_df = mars_df.columns=['Description', 'Mars', 'Earth']
    # drop index
    mars_df = mars_df.set_index('Description', inplace=True)

    mars_html = mars_df.to_html()

    ###############################
    # Hemispheres
    ###############################

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    image_urls = []

    # https://splinter.readthedocs.io/en/latest/finding.html
    # allows us to only target links on a webpage

    links = browser.find_by_css("a.product-item img")


    for link in range(len(links)):
        hemisphere = {}
        
        # click on image, get ref
        browser.find_by_css("a.product-item img")[link].click()
        sample_elem = browser.links.find_by_text("Sample").first
        hemisphere["img"] = sample_elem["href"]
        
        # get the title and append to list
        hemisphere["title"] = browser.find_by_css("h2.title").text
        image_urls.append(hemisphere)
        
        # .back() so loop does not fail
        browser.back()

    # End browser connection
    browser.quit

    # Single dictionary
    mars_data = {
        'headline': title, 
        'text': paragraph,
        'JPL_image': image_url,
        'mars_facts': mars_html,
        'Hemispheres': hemisphere
    }

    return mars_data