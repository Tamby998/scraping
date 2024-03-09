from __future__ import annotations

import sys
import re
from typing import List
from urllib.parse import urljoin

from selectolax.parser import HTMLParser
from loguru import logger
import sys
import requests

logger.remove()
logger.add("books.log", rotation="500kb", level="WARNING")
logger.add(sys.stderr, level="INFO")

BAS_URL = "https://books.toscrape.com/index.html"

def get_all_books_urls(url: str) -> List[str]:
    """
    Recupere toutles les URLs des livres sur toutes les pages à partir d'une URL
    :param url: URL de depart
    :return: liste de toutes les URLs de toutes les pages
    """
    urls = []

    while True:
        logger.info(f"Début du scrapping pour la page: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la requête HTTP sur la page {url}: {e}")
            continue
        tree = HTMLParser(response.text)
        books_urls = get_all_books_urls_on_page(url, tree)
        urls.extend(books_urls)

        url = get_next_page_url(url, tree)
        if not url:
            break


    return urls

def get_next_page_url(url: str, tree: HTMLParser) -> str | None:
    """
    recupere l'url de la page suivante à partir du HTML d'une page donnéé
    :param url: URL pour la page courante
    :param tree: Objet HTMLParser de la page
    :return: URL de la page suivante
    """
    next_page_node = tree.css_first("li.next > a")
    if next_page_node and "href" in next_page_node.attributes:
        return urljoin(url, next_page_node.attributes["href"])
    else:
        logger.info("Aucun bouton next trouve sur la page")
        return None



def get_all_books_urls_on_page(url: str, tree: HTMLParser) -> List[str]:
    """
    Récupère toutes les urls des livres présent sur une page.
    :param url: url de la page qui contient les livres
    :param tree: Objet HTMLParser de la page
    :return: Liste des URLs de tous les livres sur la page
    """
    try:
        books_links_nodes = tree.css("h3 > a")
        return [urljoin(url, link.attributes["href"]) for link in books_links_nodes if "href" in link.attributes]
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des URLs des livres de notre fonction {e}")
        return []

def get_book_price(url: str) -> float:
    """
    Recupere le prix d'un livre à partir de son URL
    :param url: URL de la page du livre
    :return: Prix du livre multiplie par le nombre de livres en stock
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = HTMLParser(response.text)
        price = extract_price_from_page(tree=tree)
        stock = extract_stock_quantity_page(tree=tree)
        price_stock = price * stock
        logger.info(f"Get book price at {url} : found {price_stock}")
        return price_stock
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la requête HTTP: {e}")
        return 0.0


def extract_price_from_page(tree: HTMLParser) -> float:
    """
    Extrait le prix du livre depuis le code HTML de la page
    :param tree: Objet HTMLParser de la page du livre
    :return: Le prix unitaire du livre
    """

    price_node = tree.css_first("p.price_color")
    if price_node:
        prince_string = price_node.text()
    else:
        logger.error("Aucun noeud contenant le prix n'a été trouvé")
        return 0.0
    try:
        price = re.findall(r"[0-9.]+", prince_string)[0]
    except IndexError as e:
        logger.error(f"Aucun nombre n'a été trouvé: {e}")
        return 0.0
    else:
        return float(price)


def extract_stock_quantity_page(tree: HTMLParser) -> int:
    """
    Extrait la quantite du livre en stock depuis le code HTML de la page
    :param tree: Objet HTMLParser de la page du livre
    :return: Le nombre de livre en stock
    """
    try:
        stock_node = tree.css_first("p.instock.availability")
        res = re.findall(f"\d+", stock_node.text())[0]
        return int(res)
    except AttributeError as e:
        logger.error(f"Aucun noeud 'p.instock.availability' n'a été trouvé: {e}")
        return 0
    except IndexError as e:
        logger.error(f"Aucun nombre n'a été trouvé dans le noeud: {e}")
        return 0


def main():
    base_url = "https://books.toscrape.com/index.html"
    all_books_urls = get_all_books_urls(url=base_url)
    total_price = []
    for book_url in all_books_urls:
        price = get_book_price(url=book_url)
        total_price.append(price)

    return sum(total_price)


if __name__ == '__main__':
    print(main())
