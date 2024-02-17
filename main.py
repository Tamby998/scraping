from pprint import pprint

import requests
from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
articles = soup.find_all('article', class_='product_pod')
titles_tags = soup.find_all('a', title=True)
titles = [a['title'] for a in titles_tags]
pprint(titles)