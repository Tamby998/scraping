import re


import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/index.html"
def main () -> list[int]:
    book_ids = []
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Il y a eu un problème lors de l'accès au site: {e}")
        raise requests.exceptions.RequestException from e
    soup = BeautifulSoup(response.text, "html.parser")
    one_star_books = soup.select("p.star-rating.One")
    for book in one_star_books:
        try:
            book_link = book.find_next("h3").find("a")["href"]
        except AttributeError as e:
            print(f"Impossible de trouver la balise h3: {e}")
            raise AttributeError from e
        except TypeError as e:
            print(f"Impossible de trouver la balise '<a>' à l'interieur de '<h3>' : {e}")
            raise TypeError from e
        except KeyError as e:
            print(f"Impossible de trouver la balise '<href>' à l'interieur de '<a>' : {e}")
            raise KeyError from e

        try:
            book_id = re.findall(r"_\d{1,4}", book_link)[0][1:]
        except IndexError as e:
            print(f"Impossible de recuperer les ids: {e}")
            raise IndexError from e
        else:
            book_ids.append(int(book_id))

    return book_ids
if __name__ == '__main__':
    print(main())