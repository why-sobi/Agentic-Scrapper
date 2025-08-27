import pandas as pd


def SaveResult(items: list[dict], filename: str) -> None:
    """
    Saves the scraped items to a file.
    
    Args:
        items (List[dict[str, str]]): List of dictionaries containing item details.
    """
    df = pd.DataFrame(items)

    # Ensure all expected columns exist, filling missing ones with empty strings
    expected_columns = ['name', 'URL', 'price', 'rating', 'description', 'website']
    for col in expected_columns:
        if col not in df:
            df[col] = ''
    
    # Reorder columns to maintain consistency
    df = df[expected_columns]

    df.to_csv(filename, index=False)

    return f"Items saved successfully to {filename}"

if __name__ == "__main__":
    pass  # This module is not meant to be run directly
    # It is intended to be imported and used in other modules.