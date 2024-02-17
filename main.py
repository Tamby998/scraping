import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Fonction pour parcourir récursivement l'arbre du DOM

def traverse_dom(element, level=0):
    # Afficher l'élément actuel
    if element.name:
        print(f"{' ' * level}<{element.name}>")

    # Si l'élément a des enfants, les parcourir egalement
    if hasattr(element, 'children'):
        for child in element.children:
            traverse_dom(child, level + 1)

# Commencer le parcours depuis la racine de l'arbre DOM
traverse_dom(soup)