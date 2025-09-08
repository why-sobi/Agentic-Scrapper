from playwright.sync_api import sync_playwright
from time import sleep
from bs4 import BeautifulSoup

from scrapperUtils import clean_text

URL = 'https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&st={product}&intl=nosplash'
PRODUCT = '.sku-block'
PRODUCT_LINK = '.product-list-item-link'
# To get name use inner text of beautifulSoup to extract it from the <a><a/> of the product link
RATING = '.font-weight-medium.font-weight-bold.order-1' # its a span tag with this class (to further specify what HTML tag are we reffering to)
PRICE = 'span.font-sans.text-default.text-style-body-md-400.font-500.text-7.leading-7'
NAME = '.h4.mb-200'
# -------- ALl this after opening the link ----------
# Scroll then click this button
FEATURES = '.ZjQDoW6pq08UwL3A'
GENERAL_DETAILS = '.mb-200 p' # p-tag inside the class mb-200
MORE_DETAILS = '.pl-300' # it'll be an unordered list (use BeautifulSoup to extract the inner text)

def BestBuyScraper(product_name: str, num: int = 5) -> list[dict]:
    result = []
    product_links = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto(URL.format(product=product_name), timeout=50000)
        sleep(20)
        
        page.wait_for_selector(PRODUCT)
        while len(product_links) < num:
            products = page.query_selector_all(PRODUCT)
            for product in products:
                product_links.append(product.query_selector(PRODUCT_LINK).get_attribute('href'))
                if len(product_links) >= num:
                    break
        
        for link in product_links:
            page.goto(link, timeout=50000)
            sleep(5)

            name = page.query_selector(NAME).inner_text()          
            rating = page.query_selector(RATING).inner_text() + '/5'
            price = page.query_selector(PRICE).inner_text()
            
            page.mouse.wheel(0, 600)
            sleep(5)
            
            features_button = page.query_selector(FEATURES)
            features_button.click()
            sleep(5)
            
            description = page.query_selector(GENERAL_DETAILS).inner_text()
            
            result.append({
                "name": clean_text(name),
                "price": price,
                "URL": link,
                "rating": rating,
                "description": clean_text(description),
                'website': "BestBuy America"
            })
            
    return result

if __name__ == "__main__":
    print(BestBuyScraper("Nvidia"))