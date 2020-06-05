from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

baseURL = 'https://forum.flowster.app'

# Open Chrome web client using Selenium and retrieve page source
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome( \
    executable_path = r'C:\Users\kevin\Desktop\chromedriver_win32\chromedriver.exe', \
    chrome_options = options)

driver.get(baseURL)
baseHTML = driver.page_source

# Get base HTML text and generate soup object
#baseHTML = requests.get(baseURL).text
baseSoup = BeautifulSoup(baseHTML, 'html.parser')

#print(baseSoup.prettify())

# Find all anchor objects that contain category information
categoryAnchors = baseSoup.find_all('a', class_='category-title-link')

# Get hyperlink reference and append it to the base URL to get the category page URL
href = categoryAnchors[0]['href']
categoryPageURL = baseURL + href

print(categoryPageURL)

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
print(topicName)

# Get topic category and tags
topicCategoryDiv = topicSoup.find('div', class_='topic-category ember-view')

tagAnchors = topicCategoryDiv.find_all('span', class_='category-name')

for anchor in tagAnchors:
    print(anchor.text)




'''
for topic in topicAnchors:
    href = topic['href']
    print(href)
'''

''' Non-Selenium Implementation
# Find all table cells that belong to the category class
categoryCells = baseSoup.find_all('td', class_='category')

# Get hyperlink reference and append it to the base URL to get the category page URL
href = categoryCells[0].div.h3.a['href']
categoryPageURL = baseURL + href

print(categoryPageURL)

# Get category HTML text and generate soup object
categoryHTML = requests.get(categoryPageURL).text
categorySoup = BeautifulSoup(categoryHTML, 'html.parser')

topicCells = categorySoup.find_all('td', class_='main-link')

for topic in topicCells:
    href = topic.a['href']
    print(href)
'''
