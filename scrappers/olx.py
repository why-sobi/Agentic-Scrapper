from playwright.sync_api import sync_playwright
from scrappers.scrapperUtils import clean_text

import time
import sys
import json

WEBSITE_URL = "https://www.olx.com.pk"


def scrape_urls(links: list[str]) -> list[dict]:
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        i = 0
        while  i < len(links):
            page.goto(links[i], wait_until="domcontentloaded")
            print("Here")
            while "error.html" in page.url:
                page.goto(links[i], wait_until="domcontentloaded")
                print("still sleeping")
                time.sleep(5)
            
            try:
                price = clean_text(page.locator("._24469da7").inner_text()) or None
                name = clean_text(page.locator("._75bce902").inner_text()) or None
                description = clean_text(page.locator("._7a99ad24").inner_text()) or None
                results.append({
                    "name": name,
                    "URL": links[i],
                    "price": price if price else "",
                    "description": description,
                    "rating": "",
                    "website": "Olx"
                })
                i += 1
            except Exception as e:
                continue
        browser.close()
    return results

def OlxScrapper(product_name: str, num_of_products: int = 10) -> list[dict]:
    """
    Scrapes OLX for product links.
    
    Args:
        product_name: The search keyword.
        num_of_products: Number of product links to fetch (default=50).
    
    Returns:
        List of product URLs.
    """
    def build_search_url(query: str, page_number: int = 0) -> str:
        base_url = WEBSITE_URL + "/items/q-" + query.replace(" ", "-")
        return base_url if page_number == 0 else f"{base_url}?page={page_number}"

    product_links = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page_number = 0
        page.goto(build_search_url(product_name, page_number))
        while len(product_links) < num_of_products:
            print("Maybe Here")
            while "error.html" in page.url:
                time.sleep(5)
                browser.close()
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(build_search_url(product_name, page_number))
                print("still sleeping")
                time.sleep(5)
            try:
                button = page.locator("#optInText")
                if button.is_visible():
                    button.click()
            except Exception as e:
                pass
            # Grab all product <li> elements
            ul = page.locator("ul._1aad128c.ec65250d")
            items = ul.locator('xpath=/li').all()
            for item in items:
                href = item.locator("a").first.get_attribute("href")
                if not href:
                    continue
                if href.startswith(WEBSITE_URL):  # skip ads
                    continue

                product_links.add(WEBSITE_URL + href)
                if len(product_links) >= num_of_products:
                    break
            if len(items) > 0:
                page_number += 1

    return json.dumps(scrape_urls(list(product_links)))
            
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(OlxScrapper(sys.argv[1],int(sys.argv[2])))
    else:
        print(OlxScrapper(sys.argv[1]))
