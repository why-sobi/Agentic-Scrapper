from playwright.sync_api import sync_playwright
import sys

WEBSITE_URL = "https://www.olx.com.pk"

class Product():
    def __init__(self,name,link,):
        self.name = name
        self.link = link

    def get_product(self):
        pass

def scrape_url(link: str):
    pass

def run(input_query: str, num_of_products: int = 50) -> list[dict]:

    with sync_playwright() as p:
        # Launch a browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Go to the target site
        url = WEBSITE_URL + "/items/q-"+input_query.replace(" ","-")
        page.goto(url)
        
        # Example: Extract all the List items
        product_links = set()
        page_number = 0

        while(True):
            # Get the items list using class name
            ul = page.locator("xpath=/html/body/div/div[1]/header[2]/div/div/div/div[2]/div[2]/div[2]/div/div/div[3]/ul")
            get_list_items = ul.locator('xpath=/li').all()
            # Loop through Items and extract link
            for item in get_list_items:
                link = item.locator("a").first          # Get the First <a> tag  
                href = link.get_attribute("href")       # Get the First href for url
                if "https://www.olx.com.pk" in href:    # Filter out adds by using their URL
                    continue
                else:
                    full_link = "https://www.olx.com.pk" + href
                    product_links.add(full_link)
                if(len(product_links) >= num_of_products):
                    browser.close()
                    return product_links
            
            # If the length is not yet fulfilled, move towards the next page
            page_number += 1
            page.goto(url + f"?page={page_number}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(run(sys.argv[1],int(sys.argv[2])))
    else:
        print(run(sys.argv[1]))