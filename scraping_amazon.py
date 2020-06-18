import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

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
    body = soup.find('body')
    all_a = body.findAll('a', {'itemprop': "item"})

    print('collecting all category links')
    category_links = []
    for a in all_a:
        href = a.get('href')
        link = 'https://sellercentral.amazon.com' + href
        category_links.append(link)

    for link in category_links:
        if len(link) <= len('https://sellercentral.amazon.com/forums/c/'):
            category_links.remove(link)
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
    df_post.to_csv('amazon_forum_post_links.csv')