from pprint import pprint
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/index.html"
def main (threshold: int = 5):
    with requests.Session() as session:

        response = session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        categories = soup.find('ul', class_="nav nav-list").find_all("a")
        categories_url = [category["href"] for category in categories[1:]]

        # Naviguer dans les url
        for category_url in categories_url:
            absolute_url = urljoin(BASE_URL, category_url)
            response = session.get(absolute_url)
            soup = BeautifulSoup(response.text, "html.parser")

            books = soup.select("article.product_pod")
            number_of_book = len(books)
            category_title = soup.select_one("h1").text
            if number_of_book <= threshold:
                print(f"La catégorie '{category_title}' ne contient pas assez de livre '{number_of_book}'")
            else:
                print(f"La catégorie '{category_title}' contient assez de livres '{number_of_book}'")
if __name__ == '__main__':
    main(threshold=1)