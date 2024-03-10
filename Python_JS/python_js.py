from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.docstring.fr/scraping/")

    page.locator("css=#get-secrets-books").click()
    page.wait_for_timeout(2000)
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    for titre in soup.select("h2"):
        print(titre.text)
    browser.close()
