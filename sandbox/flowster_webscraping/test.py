from bs4 import BeautifulSoup
import requests

sourceHTML = requests.get('https://forum.flowster.app/').text

soup = BeautifulSoup(sourceHTML, 'html.parser')

#print(soup.prettify())

anchors = soup.find_all('a')

for anchor in anchors:
    print(anchor['href'])


