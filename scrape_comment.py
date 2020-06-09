import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

df_post = pd.read_csv("amazon_forum_post_links.csv")

#this method returns the category aka the tag of the webpage
def get_category():
    body = soup.find('body')
    category_name = body.find('span').getText()
    return category_name

#this method returns a string containing the author of the post
def get_post_author():
    creators = soup.findAll(class_="creator")
    post_author=creators[0].find('a').getText()
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
    post_title = body.find_all('h1')[0].find('a').getText().strip()
    return post_title

#this method returns a string of the leading comment of the post
def get_leading_comment():
    comments = soup.findAll(class_="post")
    #We just need the first comment here
    leading_comment = comments[0].getText().strip()
    return leading_comment

#this method returns an array of strings of the reply comments
def get_reply_comments():
    comments = soup.findAll(class_="post")
    comments_arr=[]
    #Look through all the comments except the first which is the leading comment
    for comment in comments[1:]:
      comments_arr.append(comment.getText().strip())
    return comments_arr


#this method returns the time the post was published
def get_published_time():
    times = soup.findAll("time")
    publish_time = times[0].getText().strip()
    return publish_time

#this method returns the times for all the replies in an array of type string
def get_reply_times():
    times = soup.findAll("time")
    reply_times = []
    for time in times[1:]:
        reply_times.append(time.getText().strip())
    return reply_times


row_list= []
i = 0
for link in df_post['post_link']:
  try:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    curr_row = {'Link': link, 'Title':get_post_title(), 'Category':get_category(), 'Post Author':get_post_author(), 'Leading Comment':get_leading_comment(), 'Publish Time':get_published_time(), 'Reply Authors':get_reply_authors, 'Reply Comments':get_reply_comments(), 'Reply Times':get_reply_times()}
    row_list.append(curr_row)
    i=i+1
    if(i%10==0):print(i)
  except AttributeError:
    continue

scraped_data = pd.DataFrame(row_list)
scraped_data.to_csv('amazon_scraped_data.csv')
