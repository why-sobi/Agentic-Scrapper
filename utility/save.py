import pandas as pd

def SaveResult(items: list[dict], filename: str) -> None:
    """
    Saves the scraped items to a file.
    
    Args:
        items (List[dict[str, str]]): List of dictionaries containing item details.
    """
    products_list = {'name': [], 'url': [], 'price': [], 'rating': [], 'description': []}
    for item in items:
        products_list['name'].append(item.get('name', ''))
        products_list['url'].append(item.get('URL', ''))
        products_list['price'].append(item.get('price', ''))
        products_list['rating'].append(item.get('rating', ''))
        products_list['description'].append(item.get('description', ''))
        
    df = pd.DataFrame.from_dict(products_list)
    df.to_csv(filename, index=False) 

    return f"Items saved successfully to {filename}"

if __name__ == "__main__":
    pass  # This module is not meant to be run directly
    # It is intended to be imported and used in other modules.