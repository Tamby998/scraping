from pprint import pprint

import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
aside = soup.find('div', class_="side_categories")
categories_div = aside.find("ul").find('li').find('ul')
categories = [child.text.strip() for child in categories_div.children if child.name]

images = soup.find('section').find_all('img')
for image in images:
    print(image['src'])
