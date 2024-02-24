import sys
from typing import List

from selectolax.parser import HTMLParser
from loguru import logger
import sys

logger.remove()
logger.add("books.log", rotation="500kb", level="WARNING")
logger.add(sys.stderr, level="INFO")


def get_all_books_urls(url: str) -> List[str]:
    """
    Recupere toutles les URLs des livres sur toutes les pages à partir d'une URL
    :param url: URL de depart
    :return: liste de toutes les URLs de toutes les pages
    """
    pass


def get_next_page_url(tree: HTMLParser) -> str:
    """
    recupere l'rul de la page suivante à partir du HTML d'une page donnéé
    :param tree: Objet HTMLParser de la page
    :return: URL de la page suivante
    """
    pass


def get_all_books_urls_on_page(tree: HTMLParser) -> List[str]:
    """
    Récupère toutes les urls des livres présent sur une page.
    :param tree: Objet HTMLParser de la page
    :return: Liste des URLs de tous les livres sur la page
    """
    pass


def get_book_price(url: str) -> float:
    """
    Recupere le prix d'un livre à partir de son URL
    :param url: URL de la page du livre
    :return: Prix du livre multiplie par le nombre de livres en stock
    """
    pass


def extract_price_from_page(tree: HTMLParser) -> float:
    """
    Extrait le prix du livre depuis le code HTML de la page
    :param tree: Objet HTMLParser de la page du livre
    :return: Le prix unitaire du livre
    """
    pass


def extract_stock_quantity_page(tree: HTMLParser) -> int:
    """
    Extrait la quantite du livre en stock depuis le code HTML de la page
    :param tree: Objet HTMLParser de la page du livre
    :return: Le nombre de livre en stock
    """
    pass


def main():
    BASE_URL = "https://books.toscrape.com/index.html"
    all_books_urls = get_all_books_urls(url=BASE_URL)
    total_price = []
    for book_url in all_books_urls:
        price = get_book_price(url=book_url)
        total_price.append(price)

    return sum(total_price)

if __name__ == '__main__':
    print(main())
