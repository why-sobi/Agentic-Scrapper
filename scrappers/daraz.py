from playwright.sync_api import sync_playwright
from time import sleep
from bs4 import BeautifulSoup
import sys

from scrappers.scrapperUtils import clean_text

URL = 'https://www.daraz.pk/catalog/?q={product}'
SEARCHBOX_ID = '#q' 
INFO_CONTAINER_CLASS = '.buTCk'

LINK_CLASS = '.RfADt' # it is inside info container and it encompasses the link (a-tag) to the product along with it's title
RATING_CHECKBOX_CLASS = '.mdmmT._32vUv' # if this class exists, it means that the product has a rating

NAME_CLASS = '.pdp-mod-product-badge-title' 
PRICE_CLASS = '.notranslate.pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl' # it is inside info container and it encompasses the price (span-tag) of the product
RATING_CLASS = '.score-average' # after opening the link a span with this class contains the rating of the product
DESCRIPTION_CLASS = '.html-content.pdp-product-highlights' # article tag with p-tags and span tags (\n will be used after p-tags are closed and span-tags content will be concatenated)
MAX_RATING = '5'

def DarazScrapper(product_name: str, num: int = 10) -> list[dict]:
    """
    Scrapes Daraz for the given product name and returns a list of dictionaries with the results.
    
    Args:
        product (str): The name of the product to search for on Daraz.
        
    Returns:
        list[dict]: A list of dictionaries containing the scraped data.
    """
    
    result = []
    product_links = []
    ratings = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL.format(product=product_name))
        
        page.wait_for_selector(INFO_CONTAINER_CLASS)
        
        while len(product_links) < num:
            products = page.query_selector_all(INFO_CONTAINER_CLASS)
            for product in products:
                product_links.append('https:' + product.query_selector(LINK_CLASS + ' a').get_attribute('href'))
                ratings.append(True if product.query_selector(RATING_CHECKBOX_CLASS) else False)

                if len(product_links) >= num:
                    break
                
        for i, link in enumerate(product_links):
            page.goto(link, timeout=50000)
            
            name = page.query_selector(NAME_CLASS).inner_text().strip()
            price = page.query_selector(PRICE_CLASS).inner_text().strip()
            
            page.mouse.wheel(0, 1200)
            
            if ratings[i]:
                page.wait_for_selector(RATING_CLASS)
                rating_element = page.query_selector(RATING_CLASS)
                if rating_element:
                    ratings[i] = rating_element.inner_text().strip()
                else:
                    ratings[i] = "No rating available"
            else:
                ratings[i] = "No rating available"
            
            page.wait_for_selector(DESCRIPTION_CLASS, timeout=50000)
            description_element = page.query_selector(DESCRIPTION_CLASS)
            
            description = BeautifulSoup(description_element.inner_html(), features='html.parser')
            description = description.get_text(separator=' ')
            
            result.append({
                    "name": clean_text(name),
                    "price": price,
                    "URL": link,
                    "rating": ratings[i],
                    "description": clean_text(description),
                    'website': "Daraz"
            })
            
        
        browser.close()
    
    return result
        

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(OptimizedScraper(sys.argv[1],int(sys.argv[2])))
    else:
        print(OptimizedScraper(sys.argv[1]))
    pass  # This module is not meant to be run directly
    # It is intended to be imported and used in other modules.
    results = DarazScrapper('Xbox One')
    for result in results:
        print(result)