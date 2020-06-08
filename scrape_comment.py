import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd


response = requests.get('https://sellercentral.amazon.com/forums/t/shipping/639627')

if response: 
  print('Success!')
else:
  print('An error has occurred.')   

soup = BeautifulSoup(response.text, 'html.parser')

print(soup.prettify())

body = soup.find('body')
# get post title
post_title = body.find_all('h1')[0].find('a').getText()

category_name = body.find('span').getText()

creators = soup.findAll(class_="creator")
comments = soup.findAll(class_="post")

post_author = creators[0].find('a').getText()
leading_comment = comments[0].getText()

creator_arr=[];
dates_arr=[];
comments_arr=[];

# get authors of replies
for creator in creators[1:]:
  creator_arr.append(creator.find('a').getText())


for x in creator_arr:
  print(x)

# get contents of replies
for comment in comments[1:]:
  comments_arr.append(comment.getText())




