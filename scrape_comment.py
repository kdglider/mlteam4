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


#this method returns the category aka the tag of the webpage
def get_category():
    body = soup.find('body')
    category_name = body.find('span').getText()
    return category_name



#this method returns a string containing the author of the post
def get_post_author():
    creators = soup.findAll(class_="creator")
    post_author = creators[0].find('a').getText()
    return post_author

#this method returns an array containing a list of the authors of the replies
def get_reply_authors():
    creators = soup.findAll(class_="creator")
    creator_arr = []
    for creator in creators[1:]:
        creator_arr.append(creator.find('a').getText())
    return creator_arr
    

#this method returns the title of the post
def get_post_title():
    body = soup.find('body')
    #getting the title
    post_title = body.find_all('h1')[0].find('a').getText()
    return post_title

#this method returns a string of the leading comment of the post
def get_leading_comment():
    comments = soup.findAll(class_="post")
    #We just need the first comment here
    leading_comment = comments[0].getText()
    return leading_comment

#this method returns an array of strings of the reply comments
def get_reply_comments():
    comments = soup.findAll(class_="post")
    comments_arr=[]
    #Look through all the comments except the first which is the leading comment
    for comment in comments[1:]:
        comments_arr.append(comment.getText())
    return comments


#this method returns the time the post was published
def get_published_time():
    times = soup.findAll("time")
    publish_time = times[0].getText()
    return publish_time

#this method returns the times for all the replies in an array of type string
def get_reply_times():
    times = soup.findAll("time")
    reply_times = []
    for time in times[1:]:
        reply_times.append(time.getText())
    return reply_times
