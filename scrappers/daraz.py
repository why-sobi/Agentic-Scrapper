from playwright.sync_api import sync_playwright
from time import sleep
from bs4 import BeautifulSoup

from scrappers.scrapperUtils import clean_text

URL = 'https://www.daraz.pk/catalog/?q={product}'
SEARCHBOX_ID = '#q' 
INFO_CONTAINER_CLASS = '.buTCk'
LINK_CLASS = '.RfADt' # it is inside info container and it encompasses the link (a-tag) to the product along with it's title
PRICE_CLASS = '.aBrP0' # it is inside info container and it encompasses the price (span-tag) of the product

RATING_CHECKBOX_CLASS = '.mdmmT._32vUv' # if this class exists, it means that the product has a rating
RATING_CLASS = '.score-average' # after opening the link a span with this class contains the rating of the product
DESCRIPTION_CLASS = '.html-content.pdp-product-highlights' # article tag with p-tags and span tags (\n will be used after p-tags are closed and span-tags content will be concatenated)
MAX_RATING = '5'

def DarazScrapper(product: str, num: int = 10) -> list[dict]:
    """
    Scrapes Daraz for the given product name and returns a list of dictionaries with the results.
    
    Args:
        product (str): The name of the product to search for on Daraz.
        
    Returns:
        list[dict]: A list of dictionaries containing the scraped data.
    """
    
    result = []
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(URL.format(product=product))
                
        page.wait_for_selector(INFO_CONTAINER_CLASS)
        
        for i in range(num):
            container = page.query_selector_all(INFO_CONTAINER_CLASS)[i]
            
            link_element = container.query_selector(LINK_CLASS + ' a')
            price_element = container.query_selector(PRICE_CLASS)
            hasRating = True if container.query_selector(RATING_CHECKBOX_CLASS) else False
            
            if link_element and price_element:
                product_link = "https:" + link_element.get_attribute('href')  
                product_name = link_element.inner_text().strip()
                product_price = price_element.inner_text().strip()
                                
                # Navigate to the product page to get more details
                page.goto(product_link, timeout=50000)
                sleep(3)
                
                # Get the rating if available
                page.mouse.wheel(0, 1000)  # Scroll down to load the description
                sleep(2)  # Wait for the description to load
                
                if hasRating:
                    rating_element = page.query_selector(RATING_CLASS)
                    if rating_element:
                        product_rating = rating_element.inner_text().strip()
                    else:
                        product_rating = "No rating available"
                else:
                    product_rating = "No rating available"
                    
                
                # Get the description
                page.wait_for_selector(DESCRIPTION_CLASS, timeout=50000)
                description_element = page.query_selector(DESCRIPTION_CLASS)
                
                description = BeautifulSoup(description_element.inner_html(), features='html.parser')
                description = description.get_text(separator=' ')
                                
                # Append the product details to the result list
                result.append({
                    "name": clean_text(product_name),
                    "price": product_price,
                    "URL": product_link,
                    "rating": product_rating,
                    "description": clean_text(description),
                    'website': "Daraz"
                })
                
                page.go_back()  # Go back to the search results page
                sleep(2)  # Wait for the page to load again
                
        browser.close()
        
    return result

if __name__ == "__main__":
    pass  # This module is not meant to be run directly
    # It is intended to be imported and used in other modules.