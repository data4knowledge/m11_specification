import re
from pathlib import Path
from raw_docx import RawDocx, RawDocument, RawParagraph, RawTable, RawSection

class M11Template:

    def __init__(self, filepath: str):
        """
        Initialize the M11 processor with paths to both specification documents.

        Args:
            filepath (str): Path to the Template Specification PDF
        """
        self.document = None
        self.elements = []
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(
                f"Template specification file not found: {filepath}"
            )

    def process(self) -> None:
        """
        Process the template specification document.
        """
        raw_doc: RawDocument = RawDocx(self.filepath).target_document
        self.document = raw_doc.to_dict()
        for section in raw_doc.sections:
            for item in section.items:
                if isinstance(item, RawParagraph):
                    confirmed_elements = self._extract_elements(section, item)
                    self.elements += confirmed_elements
                elif isinstance(item, RawTable):
                    for row in item.rows:
                        for cell in row.cells:
                            for item in cell.items:
                                if isinstance(item, RawParagraph):
                                    confirmed_elements = self._extract_elements(section, item)
                                    self.elements += confirmed_elements
    
    def _extract_elements(self, section: RawSection, paragraph: RawParagraph) -> list[str]:
        """
        Extract elements from a paragraph.

        Args:
            section (RawSection): The section the paragraph belongs to
            paragraph (RawParagraph): The paragraph to extract elements from

        Returns:
            list[str]: A list of confirmed elements
        """
        confirmed_elements = []
        potential_elements = self._find_elements(paragraph.text)
        for element in potential_elements:
            print(f"TEXT: {[x.text for x in paragraph.runs]}")
            print(f"COLOR: {[x.color for x in paragraph.runs]}")
            print(f"HIGHLIGHT: {[x.highlight for x in paragraph.runs]}")
            print(f"STYLE: {[x.style for x in paragraph.runs]}")
            match = next((x for x in paragraph.runs if element in x.text and x.highlight == 'GRAY_25 (16)'), None)
            if match:
                short_name = element.replace("Enter ", "")
                confirmed_elements.append({'long_name': element, 'short_name': short_name, 'section_number': section.number, 'section_title': section.title})
        print(f"CONFIRMED ELEMENTS: {confirmed_elements}")  
        return confirmed_elements
    
    def _find_elements(self, text: str) -> list[str]:
        """
        Find elements in a paragraph. 
        Elements are found by looking for text between < and >.
        Args:
            text (str): The text to find elements in

        Returns:
            list[str]: A list of elements
        """
        pattern = r'<([^>]+)>'
        matches = re.findall(pattern, text)
        print(f"MATCHES: {matches}")
        return matches