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
        self.elements = {}
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
                last_document_elements = []
                if isinstance(item, RawParagraph):
                    confirmed_elements = self._extract_elements(section, item)
                    if confirmed_elements:
                        self._add_elements(confirmed_elements)
                        last_document_elements = confirmed_elements
                    else:
                        instructions = self._extract_instructions(section, item)
                        self._add_instructions(last_document_elements, instructions)
                        last_document_elements = []
                elif isinstance(item, RawTable):
                    for row in item.rows:
                        for cell in row.cells:
                            last_row_elements = []
                            for item in cell.items:
                                if isinstance(item, RawParagraph):
                                    confirmed_elements = self._extract_elements(
                                        section, item
                                    )
                                    self._add_elements(confirmed_elements)
                                    last_row_elements = confirmed_elements
                                    instructions = self._extract_instructions(
                                        section, item
                                    )
                                    self._add_instructions(
                                        last_row_elements, instructions
                                    )

    def _add_elements(self, elements: list[str]) -> None:
        """
        Add elements to the elements dictionary.
        """
        for element in elements:
            self.elements[element["short_name"]] = element

    def _add_instructions(self, elements: list[str], instructions: list[str]) -> None:
        """
        Add instructions to the elements dictionary.
        """
        for element in elements:
            element["instructions"] = instructions

    def _extract_elements(
        self, section: RawSection, paragraph: RawParagraph
    ) -> list[str]:
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
            # print(f"TEXT: {[x.text for x in paragraph.runs]}")
            # print(f"COLOR: {[x.color for x in paragraph.runs]}")
            # print(f"HIGHLIGHT: {[x.highlight for x in paragraph.runs]}")
            # print(f"STYLE: {[x.style for x in paragraph.runs]}")
            match = next(
                (
                    x
                    for x in paragraph.runs
                    if element in x.text and x.highlight == "GRAY_25 (16)"
                ),
                None,
            )
            if match:
                short_name = element.replace("Enter ", "")
                optional = True if match.color == "3333FF" else False
                confirmed_elements.append(
                    {
                        "long_name": element,
                        "short_name": short_name,
                        "optional": optional,
                        "section_number": section.number,
                        "section_title": section.title,
                        "optional": optional,
                        "instructions": []
                    }
                )
        print(f"CONFIRMED ELEMENTS: {confirmed_elements}")
        return confirmed_elements

    def _extract_instructions(
        self, section: RawSection, paragraph: RawParagraph
    ) -> list[str]:
        """
        Extract instructions from a paragraph.

        Args:
            section (RawSection): The section the paragraph belongs to
            paragraph (RawParagraph): The paragraph to extract instructions from

        Returns:
            list[str]: The instructions
        """
        instructions = [x.text for x in paragraph.runs if x.color == "C00000"]
        print(f"INSTRUCTIONS: {instructions}")
        return instructions

    def _find_elements(self, text: str) -> list[str]:
        """
        Find elements in a paragraph.
        Elements are found by looking for text between < and >.
        Args:
            text (str): The text to find elements in

        Returns:
            list[str]: A list of elements
        """
        pattern = r"<([^>]+)>"
        matches = re.findall(pattern, text)
        # print(f"MATCHES: {matches}")
        return matches
