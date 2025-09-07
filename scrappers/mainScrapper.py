from scrappers.daraz import DarazScrapper
from scrappers.olx import OlxScrapper
import json

def scrapper(product_name):
    products = None
    # products = DarazScrapper(product_name)
    return OlxScrapper(product_name)
    olx_products = OlxScrapper(product_name)
    products.extend(olx_products)
    return json.dumps(products)

if __name__ == "__main__":
    pass