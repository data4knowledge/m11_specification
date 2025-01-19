import re


def clean_element_name(element_name: str) -> str:
    """
    Clean the element name. Remove any non-alphanumeric characters.
    """
    return re.sub(r'[^a-zA-Z0-9 ]', '', element_name).strip()