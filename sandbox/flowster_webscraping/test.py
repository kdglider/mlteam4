from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import pandas


#####Functions:#####
'''
def get_leadc(topicSoup):
    for c in topicSoup.find_all('meta', property='og:description'):
        leadc = c.get('content')
        return leadc
    
def get_otherc(topicSoup):
    postStream = topicSoup.find('div', class_='post-stream')
    postDivs = postStream.find_all('div', {'class':['topic-post clearfix regular','topic-post clearfix topic-owner regular']})
    otherc = []
    for i in range(1, len(postDivs)):
        post = postDivs[i].find('div', class_='cooked').text
        otherc.append(post)
    return otherc
'''

def get_comments(topicSoup):
    postStream = topicSoup.find('div', class_='post-stream')
    postDivs = postStream.find_all('div', {'class':['topic-post clearfix regular','topic-post clearfix topic-owner regular']})
    comments = []
    for i in range(1, len(postDivs)):
        comment = postDivs[i].find('div', class_='cooked').text
        comments.append(comment)
    leadingComment = comments[0]
    otherComments = comments[1:]
    return leadingComment, otherComments
    
def get_category_and_tags(topicSoup):
    temp_tag = []
    for n in topicSoup.find_all('span', class_="category-name"):
        temp_tag.append(n.getText())
    return temp_tag[0], temp_tag[1:]

def get_title(topicSoup):
    topicName = topicSoup.find('a', class_='fancy-title').text
    return topicName
    
def get_author_and_commenters(topicSoup):
    names = topicSoup.find_all("span", class_="creator")
    authorList=[]
    for name in names:
        name = a.getText()
        authorList.append(name.strip())
    return authorList[0], authorList[1:]

def get_views(topicSoup):
    views = topicSoup.find('li', class_='secondary views')
    if views == None:
        return str(0)
    return views.span.text
    
def get_likes(topicSoup):
    likes = topicSoup.find('li', class_='secondary likes')
    if likes == None:
        return str(0)
    return likes.span.text



if __name__=='main':
    # Local path to webdriver
    webdriverPath = r'C:\Users\kevin\Desktop\chromedriver_win32\chromedriver.exe'

    # Set up webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')     # Ignore security certificates
    options.add_argument('--incognito')                     # Use Chrome in Incognito mode
    options.add_argument('--headless')                      # Run in background
    driver = webdriver.Chrome( \
        executable_path = webdriverPath, \
        options = options)

    # Flowster forum base URL
    baseURL = 'https://forum.flowster.app'

    # Open Chrome web client using Selenium and retrieve page source
    driver.get(baseURL)
    baseHTML = driver.page_source

    # Get base HTML text and generate soup object
    baseSoup = BeautifulSoup(baseHTML, 'html.parser')

    #print(baseSoup.prettify())

    # Find all anchor objects that contain category information
    categoryAnchors = baseSoup.find_all('a', class_='category-title-link')

    # Get hyperlink references and append it to the base URL to get the category page URLs
    categoryPageURLs = []
    for i in range(len(categoryAnchors)):
        href = categoryAnchors[i]['href']
        categoryPageURLs.append(baseURL + href)


    #1st for_loop ro run through all categories
    for categoryURL in categoryPageURLs:
        # Get category HTML text
        driver.get(categoryURL)

        # Load the entire webage by scrolling
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while (True):
            # Scroll to bottom of page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new page segment to load
            time.sleep(0.5)

            # Calculate new scroll height and compare with last scroll height
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight


        # Generate soup object
        categoryHTML = driver.page_source
        categorySoup = BeautifulSoup(categoryHTML, 'html.parser')

        # Find all anchor objects that contain topic information
        topicAnchors = categorySoup.find_all('a', class_='title raw-link raw-topic-link')

        # Get hyperlink references and append it to the base URL to get the topic page URLs
        
        topicPageURLs = []
        for i in range(len(topicAnchors)):
            href = topicAnchors[i]['href']
            topicPageURLs.append(baseURL + href)


        # 2nd for loop to run through all topics
        for topicURL in topicPageURLs:
            # Get category HTML text and generate soup object
            driver.get(topicURL)
            topicHTML = driver.page_source
            topicSoup = BeautifulSoup(topicHTML, 'html.parser')

            # Get topic name
            topicName = topicSoup.find('a', class_='fancy-title').text
            print('Topic Name: ' + topicName)

            # Get topic category and tags
            topicCategoryDiv = topicSoup.find('div', class_='topic-category ember-view')
            tagAnchors = topicCategoryDiv.find_all('span', class_='category-name')

            print('Topic Category: ' + tagAnchors[0].text)

            for i in range(1, len(tagAnchors)):
                print('Tag ' + str(i) + ': '+ tagAnchors[i].text)


            # Get topic author and posts
            postStream = topicSoup.find('div', class_='post-stream')
            postDivs = postStream.find_all('div', recursive=False)

            author = postDivs[0].find('span', class_='first username').a.text
            firstPost = postDivs[0].find('div', class_='cooked').text
            print('Author: ' + author)
            print('First Post: ' + '\n' + firstPost + '\n')

            for i in range(1, len(postDivs)):
                post = postDivs[i].find('div', class_='cooked').text
                print('Post ' + str(i) + ': ' + '\n' + post + '\n')



