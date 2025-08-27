from scrappers.daraz import DarazScrapper
from scrappers.olx import OlxScrapper

def scrapper(product_name):
    products = None
    products = DarazScrapper(product_name)
    olx_products = OlxScrapper(product_name)
    products.extend(olx_products)
    return products

if __name__ == "__main__":
    pass