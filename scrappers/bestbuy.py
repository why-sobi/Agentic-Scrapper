from playwright.sync_api import sync_playwright
from time import sleep
from bs4 import BeautifulSoup

from scrapperUtils import clean_text

URL = 'https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&st={product}'
PRODUCT = '.sku-block'
PRODUCT_LINK = '.product-list-item-link'
# To get name use inner text of beautifulSoup to extract it from the <a><a/> of the product link
RATING = '.font-weight-medium.font-weight-bold order-1' # its a span tag with this class (to further specify what HTML tag are we reffering to)
PRICE = '#medium-customer-price'

# -------- ALl this after opening the link ----------
# Scroll then click this button
FEATURES = '.ZjQDoW6pq08UwL3A'
GENERAL_DETAILS = '.mb-200 p' # p-tag inside the class mb-200
MORE_DETAILS = '.pl-300' # it'll be an unordered list (use BeautifulSoup to extract the inner text)

