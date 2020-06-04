from bs4 import BeautifulSoup
import requests

baseURL = 'https://forum.flowster.app'

# Get base HTML text and generate soup object
baseHTML = requests.get(baseURL).text
baseSoup = BeautifulSoup(baseHTML, 'html.parser')

#print(baseSoup.prettify())

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

