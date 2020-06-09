from bs4 import BeautifulSoup
from selenium import webdriver

import time
from datetime import datetime

import pandas as pd
import json


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

def get_title(topicSoup):
    topicName = topicSoup.find('a', class_='fancy-title').text

    # Remove leading and trailing spaces and newlines
    topicName = topicName.replace('\n', '').strip()
    return topicName


def get_category_and_tags(topicSoup):    
    topicCategoryDiv = topicSoup.find('div', class_='topic-category ember-view')
    tagAnchors = topicCategoryDiv.find_all('span', class_='category-name')

    tagList = []
    for anchor in tagAnchors:
        tagList.append(anchor.text)
    
    if (len(tagList) == 1):
        category = tagList[0]
        tags = []
        return category, tags
    else:
        category = tagList[0]
        tags = tagList[1:]
        return category, tags

    
def get_author_and_commenters(topicSoup):
    names = topicSoup.find_all("div", class_="names trigger-user-card")
    authorList = []
    for name in names:
        author = name.span.a.text
        authorList.append(author)
    
    # Remove redundant names
    authorList = list(set(authorList))

    if (len(authorList) == 1):
        author = authorList[0]
        commenters = []
        return author, commenters
    else:
        author = authorList[0]
        commenters = authorList[1:]
        return author, commenters


def get_comments(topicSoup):
    postStream = topicSoup.find('div', class_='post-stream')
    postDivs = postStream.find_all('div', \
        {'class':['topic-post clearfix regular','topic-post clearfix topic-owner regular']})

    comments = []
    for i in range(len(postDivs)):
        comment = postDivs[i].find('div', class_='cooked').text
        comments.append(comment)
    
    if (len(comments) == 1):
        leadingComment = comments[0]
        otherComments = []
        return leadingComment, otherComments
    else:
        leadingComment = comments[0]
        otherComments = comments[1:]
        return leadingComment, otherComments


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



if __name__=='__main__':
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
    
    categoryPageURLs = [categoryPageURLs[0]]

    # Set up both a dictionary and Pandas dataframe to save data to
    topicDict = {}
    topicDataframe = pd.DataFrame(columns=[
        'Topic Title', 
        'Category', 
        'Tags', 
        'Author', 
        'Commenters',
        'Leading Comment', 
        'Other Comments',
        'Likes',
        'Views'])

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

            # Scape all topic attributes of interest
            topicTitle = get_title(topicSoup)
            category, tags = get_category_and_tags(topicSoup)
            author, commenters = get_author_and_commenters(topicSoup)
            leadingComment, otherComments = get_comments(topicSoup)
            numLikes = get_likes(topicSoup)
            numViews = get_views(topicSoup)

            
            attributeDict = {
                'Topic Title'       :   topicTitle,
                'Category'          :   category,
                'Tags'              :   tags,
                'Author'            :   author,
                'Commenters'        :   commenters,
                'Leading Comment'   :   leadingComment,
                'Other Comments'    :   otherComments,
                'Likes'             :   numLikes,
                'Views'             :   numViews}
            
            topicDict[topicTitle] = attributeDict

            topicDataframe = topicDataframe.append(attributeDict, ignore_index=True)

            '''
            print('Topic Title:')
            print(topicTitle)

            print('Category:')
            print(category)

            print('Tags:')
            print(tags)

            print('Author:')
            print(author)

            print('Commenters:')
            print(commenters)

            print('Leading Comment:')
            print(leadingComment)
            
            print('Other Comments:')
            print(otherComments)

            print('Likes:')
            print(numLikes)

            print('Views:')
            print(numViews)
            '''
    

    timeStamp = datetime.now().strftime('%Y%m%d%H%M%S')
    with open('Flowster_Topic_Attributes_' + timeStamp + '.json', 'w') as f:
        json.dump(topicDict, f)

    topicDataframe.to_csv('Flowster_Topic_Attributes_' + timeStamp + '.csv')
    
    

  



