from playwright.sync_api import sync_playwright
from pydantic import BaseModel,Field
import sys

WEBSITE_URL = "https://www.olx.com.pk"

def scrape_url(link: str)-> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(link)
            price = page.locator("._24469da7[aria-label='Price']").inner_text() or None
            name = page.locator("._75bce902").inner_text() or None
            description = page.locator("._7a99ad24").inner_text() or None
        except Exception as e:
            print(e)
        browser.close()
        return {
            "name": name,
            "url": link,
            "price": price,
            "description": description,
            "rating": ""
        }


def OlxScrapper(product_name: str, num_of_products: int = 5) -> list[dict]:
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
        while len(product_links) < num_of_products:
            page.goto(build_search_url(product_name, page_number))
            
            # Grab all product <li> elements
            ul = page.locator("xpath=/html/body/div/div[1]/header[2]/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/ul")
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

            page_number += 1

        browser.close()
    scrapped_results = list(map(scrape_url,list(product_links)))
    return scrapped_results
            
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(OlxScrapper(sys.argv[1],int(sys.argv[2])))
    else:
        print(OlxScrapper(sys.argv[1]))
