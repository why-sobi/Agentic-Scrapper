from scrappers.daraz import DarazScrapper
from scrappers.olx import OlxScrapper
from scrappers.bestbuy import BestBuyScraper
import json

def scrapper(product_name):
    products = None
    products = DarazScrapper(product_name)
    olx_products = OlxScrapper(product_name)
    bestbuy_products = BestBuyScraper(product_name)
    products.extend(olx_products)
    products.extend(bestbuy_products)
    return json.dumps(products)

if __name__ == "__main__":
    pass