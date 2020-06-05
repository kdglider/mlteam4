from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

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

# Get hyperlink reference and append it to the base URL to get the category page URL
href = categoryAnchors[0]['href']
categoryPageURL = baseURL + href

# Get category HTML text
driver.get(categoryPageURL)


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

# Get hyperlink reference and append it to the base URL to get the topic page URL
href = topicAnchors[1]['href']
topicPageURL = baseURL + href

# Get category HTML text and generate soup object
driver.get(topicPageURL)
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



