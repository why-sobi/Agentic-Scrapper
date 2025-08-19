from playwright.sync_api import sync_playwright
import sys

WEBSITE_URL = "https://www.olx.com.pk"

def run(input_query: str, num_of_products: int) -> list[dict]:

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
            get_list_items = page.locator(".ec65250d li").all()
            
            # Loop through Items and extract link
            for item in get_list_items:
                print("this is item",item)
                link = item.locator("a").first          # Get the First <a> tag  
                href = link.get_attribute("href")       # Get the First href for url
                print(link,href)
                if "https://www.olx.com.pk" in href:    # Filter out adds by using their URL
                    continue
                else:
                    full_link = "https://www.olx.com.pk" + href
                    product_links.add(full_link)
            if(len(product_links) >= num_of_products):
                break
            # If the length is not yet fulfilled, move towards the next page
            page_number += 1
            page.goto(url + f"?page={page_number}", timeout=4000)
            
        browser.close()
        return product_links

if __name__ == "__main__":
    print(run(sys.argv[1],int(sys.argv[2])))
