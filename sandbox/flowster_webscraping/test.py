from bs4 import BeautifulSoup
import requests

baseURL = 'https://forum.flowster.app'

# Get source HTML text and generate soup object
sourceHTML = requests.get(baseURL).text
soup = BeautifulSoup(sourceHTML, 'html.parser')

#print(soup.prettify())

# Find all table cells that belong to the category class
categoryCells = soup.find_all('td', class_='category')

href = categoryCells[0].div.h3.a['href']

categoryPageURL = baseURL + href

print(categoryPageURL)

