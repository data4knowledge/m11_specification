import re
import yaml
from typing import Generator
from pathlib import Path
from raw_docx import RawDocx, RawDocument, RawParagraph, RawTable, RawSection
from m11_template.m11_utility import clean_element_name


class M11Template:

    START_TEXT = "This is the end of the instructional section"
    ELEMENT = "E"
    INSTRUCTION = "I"
    OTHER = "O"

    def __init__(self, filepath: str):
        """
        Initialize the M11 template processor.

        Args:
            filepath (str): Path to the Template Specification PDF
        """
        self.document = None
        self.elements = {}
        self.sections = {}
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
        state = "OUTSIDE"
        for section in raw_doc.sections:
            elements = []
            instructions = []
            section_dict = {
                "title": section.title,
                "number": section.number,
                "elements": [],
                "instructions": []
            }
            self.sections[section.number] = section_dict
            for para, reset in self._next_paragraph(section):
                print(f"PARA: {state}, {section.number}, {para.text[:20]}, {'*** RESET ***' if reset else ''}")                        
                if reset:
                    if state != "OUTSIDE":
                        if elements and instructions:
                            self._add_instructions(elements, instructions)
                        elif instructions:
                            section_dict["instructions"] += instructions
                        elements = []
                        instructions = []
                        state = "INSIDE"
                if state == "OUTSIDE":
                    if self._detect_start(para):
                        state = "INSIDE"
                        instructions += self._extract_instructions(para)
                elif state == "INSIDE":
                    para_type = self._process_para(para)
                    if para_type == self.ELEMENT:
                        elements = self._save_element(section, para)
                        state = "ELEMENT_BEFORE"
                    elif para_type == self.INSTRUCTION:
                        instructions += self._extract_instructions(para)
                        state = "INSTRUCTION_BEFORE"
                    elif para_type == self.OTHER:
                        elements = []
                        instructions = []
                elif state == "ELEMENT_BEFORE":
                    para_type = self._process_para(para)
                    if para_type == self.ELEMENT:
                        elements = self._save_element(section, para)
                        instructions = []
                        state = "ELEMENT_BEFORE"
                    elif para_type == self.INSTRUCTION:
                        self._save_instructions(elements, para)
                        state = "INSTRUCTION_AFTER"
                    elif para_type == self.OTHER:
                        elements = []
                        instructions = []
                        state = "INSIDE" # Ignore other text    
                elif state == "INSTRUCTION_BEFORE":
                    para_type = self._process_para(para)
                    if para_type == self.ELEMENT:
                        elements = self._save_element(section, para)
                        self._save_instructions(elements, para)
                        elements = []
                        instructions = []
                        state = "INSIDE" # Ignore other text    
                    elif para_type == self.INSTRUCTION:
                        instructions += self._extract_instructions(para)
                    elif para_type == self.OTHER:
                        if not elements and instructions:
                            section_dict["instructions"] += instructions
                        elements = []
                        instructions = []
                        state = "INSIDE" # Ignore other text    
                elif state == "INSTRUCTION_AFTER":                        
                    para_type = self._process_para(para)
                    if para_type == self.ELEMENT:
                        elements = self._save_element(section, para)
                        elements = []
                        instructions = []
                        state = "ELEMENT_BEFORE"
                    elif para_type == self.INSTRUCTION:
                        self._save_instructions(elements, para)
                    elif para_type == self.OTHER:
                        elements = []
                        instructions = []
                        state = "INSIDE" # Ignore other text    
                else:
                    print(f"UNKNOWN STATE: {section.number}, {para.text}")
                    state = "OUTSIDE" if state == "OUTSIDE" else "INSIDE"

    def _detect_start(self, para: RawParagraph) -> bool:
        """
        Detect the start of the definitions.
        """
        return True if para.text.startswith(self.START_TEXT) else False
        
    def _save_element(self, section: RawSection, para: RawParagraph) -> list:
        """
        Save elements to the elements dictionary.
        """
        elements = self._extract_elements(section, para)
        self._add_elements(elements)
        return elements
    
    def _save_instructions(self, elements: list, para: RawParagraph) -> list:
        """
        Save instructions to the elements dictionary.
        """
        instructions = self._extract_instructions(para)
        self._add_instructions(elements, instructions)
        return instructions

    def _process_para(self, para: RawParagraph) -> str:
        """
        Process a paragraph.
        """
        if self._has_elements(para):
            return self.ELEMENT
        elif self._has_instructions(para):
            return self.INSTRUCTION
        else:
            #print(f"OTHER: {para.text}")
            return self.OTHER

    def _next_paragraph(self, section: RawSection) -> Generator[tuple[RawParagraph, bool], None, None]:
        """
        Get the next paragraph in a section.
        """
        for item in section.items:
            if isinstance(item, RawParagraph):
                yield item, False
            elif isinstance(item, RawTable):
                for row in item.rows:
                    for cell in row.cells:
                        for index, cell_item in enumerate(cell.items):
                            if isinstance(cell_item, RawParagraph):
                                yield cell_item, index == 0


    def rename_elements(self, filepath: str) -> None:
        """
        Rename elements in the elements dictionary.
        """
        with open(filepath, "r") as f:
            rename_dict = yaml.safe_load(f)
        for key, value in rename_dict.items():
            if key in self.elements:
                self.elements[value] = self.elements[key]
                self.elements[value]["short_name"] = value
                self.elements.pop(key)

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
            self.elements[element["short_name"]]["instructions"] += instructions

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
        potential_elements = self._find_elements(paragraph)
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
                        "short_name": clean_element_name(short_name),
                        "original_name": short_name,
                        "optional": optional,
                        "section_number": section.number,
                        "section_title": section.title,
                        "instructions": [],
                    }
                )
                self.sections[section.number]["elements"].append(short_name)
        #print(f"CONFIRMED ELEMENTS: {confirmed_elements}")
        return confirmed_elements

    def _extract_instructions(
        self, paragraph: RawParagraph
    ) -> list[str]:
        """
        Extract instructions from a paragraph.

        Args:
            section (RawSection): The section the paragraph belongs to
            paragraph (RawParagraph): The paragraph to extract instructions from

        Returns:
            list[str]: The instructions
        """
        instructions = [
            x.text
            for x in paragraph.runs
            if x.color == "C00000" or x.style == "Instructional TExt"
        ]
        return instructions

    def _has_elements(self, para: RawParagraph) -> bool:
        """
        Check if a paragraph has elements.
        """
        return len(self._find_elements(para)) > 0
    
    def _has_instructions(self, para: RawParagraph) -> bool:
        """
        Check if a paragraph has instructions.
        """
        return len(self._extract_instructions(para)) > 0
    
    def _find_elements(self, para: RawParagraph) -> list[str]:
        """
        Find elements in a paragraph.
        Elements are found by looking for text between < and >.
        Args:
            text (str): The text to find elements in

        Returns:
            list[str]: A list of elements
        """
        #print(f"ELEMENT TEXT: {text}")
        pattern = r'[<\[]([^\]>]+)[\]>]'
        matches = re.findall(pattern, para.text)
        #print(f"MATCHES: {matches}")
        return matches
