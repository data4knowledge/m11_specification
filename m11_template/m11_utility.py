import re


def clean_element_name(element_name: str) -> str:
    """
    Clean the element name. Remove any non-alphanumeric characters.
    """
    text = re.sub(r'[#/%]', '-', element_name).strip()
    return re.sub(r'[^a-zA-Z0-9\- ]', '', text)

def find_elements(text: str) -> list[str]:
    """
    Find elements in a paragraph.
    Elements are found by looking for text between <>, [] and {} pairs.
    Args:
        text (str): The text to find elements in

    Returns:
        list[str]: A list of elements
    """
    #print(f"ELEMENT TEXT: {text}")
    pattern = r'[<\[]([^<\[\]>]+)[\]>]'
    matches = re.findall(pattern, text)
    #print(f"MATCHES: {matches}")
    return matches