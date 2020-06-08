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

creators = soup.findAll(class_="creator")
comments = soup.findAll(class_="post")

creator_arr=[];
dates_arr=[];
comments_arr=[];

for creator in creators:
  creator_arr.append((creator.getText()))


for x in creator_arr:
  print(x)

for comment in comments:
  comments_arr.append((comment.getText()))




