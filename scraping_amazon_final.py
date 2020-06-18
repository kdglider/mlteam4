import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# this method returns the category aka the tag of the webpage
def get_category():
    body = soup.find('body')
    category_name = body.find('span').getText()
    return category_name


# this method returns a string containing the author of the post
def get_post_author():
    creators = soup.findAll(class_="creator")
    post_author = creators[0].find('a').getText()
    return post_author


# this method returns an array containing a list of the authors of the replies
def get_reply_authors():
    creators = soup.findAll(class_="creator")
    creator_arr = []
    for creator in creators[1:]:
        creator_arr.append(creator.find('a').getText())
    return creator_arr


# this method returns the title of the post
def get_post_title():
    body = soup.find('body')
    # getting the title
    post_title = body.find_all('h1')[0].find('a').getText().strip()
    return post_title


# this method returns a string of the leading comment of the post
def get_leading_comment():
    comments = soup.findAll(class_="post")
    # We just need the first comment here
    leading_comment = comments[0].getText().strip()
    return leading_comment


# this method returns an array of strings of the reply comments
def get_reply_comments():
    comments = soup.findAll(class_="post")
    comments_arr = []
    # Look through all the comments except the first which is the leading comment
    for comment in comments[1:]:
        comments_arr.append(comment.getText().strip())
    return comments_arr


# this method returns the time the post was published
def get_published_time():
    times = soup.findAll("time")
    publish_time = times[0].getText().strip()
    return publish_time


# this method returns the times for all the replies in an array of type string
def get_reply_times():
    times = soup.findAll("time")
    reply_times = []
    for time in times[1:]:
        reply_times.append(time.getText().strip())
    return reply_times

if __name__ == "__main__":
    headers = {
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'cache-control': 'max-age=0',
    }

    base_url = 'https://sellercentral.amazon.com/forums/'
    request = requests.get(base_url, headers)
    soup = BeautifulSoup(request.text, 'lxml')
    all_a = soup.find_all('a')

    print('collecting all category links')
    category_links = []
    for a in all_a:
        href = a.get('href')
        if '/forums/c/' in href and len(href) > len('/forums/c/'):
            link = 'https://sellercentral.amazon.com' + href
            category_links.append(link)

    print('finished collecting all category links')

    print('collecting all subcategory links')
    sub_category_links = []

    for cat_link in category_links:
        request = requests.get(cat_link, headers)
        soup = BeautifulSoup(request.text, 'lxml')
        body = soup.find('body')
        main_outlet = body.find('div',{'id':"main-outlet"})
        all_a = main_outlet.findAll('a')
        for a in all_a:
            if '/forums/c/' in a.get('href'):
                link = 'https://sellercentral.amazon.com' + a.get('href')
                if (len(link) > len(cat_link)) and (link[-1].isdigit() != True):
                    sub_category_links.append(link)

    sub_category_links = list(set(sub_category_links))
    # 3 categories have no sub categories
    cat_with_no_subcat_1 = 'https://sellercentral.amazon.com/forums/c/amazon-news-us'
    cat_with_no_subcat_2 = 'https://sellercentral.amazon.com/forums/c/site-feedback'
    cat_with_no_subcat_3 = 'https://sellercentral.amazon.com/forums/c/selling-partner-success-stories'

    sub_category_links.append(cat_with_no_subcat_1)
    sub_category_links.append(cat_with_no_subcat_2)
    sub_category_links.append(cat_with_no_subcat_3)

    page_loop_url = '/l/latest?no_subcategories=false&amp;page='
    sub_category_links = [link + page_loop_url for link in sub_category_links]
    print('finished collecting all subcategory links')

    print('collecting all post links in first 10 pages of each subcategory')
    post_links = []
    for link in sub_category_links:
        for page_num in range(1,11):
            url = link + str(page_num)
            print('begin scrapping the link: ', url)
            request = requests.get(url, headers)
            soup = BeautifulSoup(request.text, 'lxml')
            body = soup.find('body')
            main_outlet = body.find('div')
            try:
                all_a = main_outlet.findAll('div', {'class': "topic-list"})[0].findAll('a')
                for a in all_a:
                    if 'http://' in a.get('href'):
                        post_link = a.get('href')
                        post_links.append(post_link)
            except AttributeError:
                continue

    df_post = pd.DataFrame(columns=['post_link'])
    df_post['post_link'] = post_links

    row_list = []

    i = 0
    for link in df_post['post_link']:
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            curr_row = {'Link': link, 'Title': get_post_title(), 'Category': get_category(),
                        'Post Author': get_post_author(), 'Leading Comment': get_leading_comment(),
                        'Publish Time': get_published_time(), 'Reply Authors': get_reply_authors,
                        'Reply Comments': get_reply_comments(), 'Reply Times': get_reply_times()}
            row_list.append(curr_row)
            i = i + 1
            if (i % 10 == 0): print(i)
        except AttributeError:
            continue

    scraped_data = pd.DataFrame(row_list)
    scraped_data.to_csv('amazon_scraped_data.csv')