import re

def clean_text(text: str)-> str:
    """
        Returns Cleaned Version of text, removing any extra weird ass characters
    """
    # Strip leading/trailing spaces
    text = text.strip()

    # Replace multiple spaces/newlines with one space
    text = re.sub(r"\s+", " ", text)

    # Escape quotes if needed (so it doesn't break JSON/Python dicts)
    text = text.replace("\n", "\\n")

    return text