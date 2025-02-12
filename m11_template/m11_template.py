import re
import yaml
from typing import Generator
from pathlib import Path
from raw_docx import RawDocx, RawDocument, RawParagraph, RawTable, RawSection, RawList
from m11_template.m11_utility import clean_element_name, find_elements


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
        self.repeat_index = 1
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
        section_title = "Title Page"
        section_number = ""
        for section in raw_doc.sections:
            elements = []
            instructions = []
            section.title = section.title if section.title else section_title
            section.number = section.number if section.number else section_number
            section_dict = {
                "title": section_title,
                "number": section_number,
                "elements": [],
                "instructions": []
            }
            self.sections[section.number] = section_dict
            for para, reset in self._next_paragraph(section):
                #print(f"\n\nPARA: {state}, {section.number}, {para.text}{', *** RESET ***' if reset else ''}")                        
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

    def rename_elements(self, filepath: str) -> None:
        with open(filepath, "r") as f:
            rename_dict = yaml.safe_load(f)
        for key, value in rename_dict.items():
            if key in self.elements:
                self.elements[value] = self.elements[key]
                self.elements[value]["short_name"] = value
                self.elements.pop(key)
            else:
                print(f"Template rename not required: {key}")

    def insert_elements(self, filepath: str) -> None:
        with open(filepath, "r") as f:
            insert_dict = yaml.safe_load(f)
        for key, value in insert_dict.items():
            if key not in self.elements:
                self.elements[key] = value

    def delete_elements(self, filepath: str) -> None:
        with open(filepath, "r") as f:
            insert_dict = yaml.safe_load(f)
        for key, value in insert_dict.items():
            if key in self.elements:
                self.elements.pop(key)
            else:
                print(f"Template delete not required: {key}")

    def _detect_start(self, para: RawParagraph) -> bool:
        return True if para.text.startswith(self.START_TEXT) else False
        
    def _save_element(self, section: RawSection, para: RawParagraph) -> list:
        elements = self._extract_elements(section, para)
        self._add_elements(elements)
        return elements
    
    def _save_instructions(self, elements: list, para: RawParagraph) -> list:
        instructions = self._extract_instructions(para)
        self._add_instructions(elements, instructions)
        return instructions

    def _process_para(self, para: RawParagraph) -> str:
        if self._has_elements(para):
            return self.ELEMENT
        elif self._has_instructions(para):
            return self.INSTRUCTION
        else:
            #print(f"OTHER: {para.text}")
            return self.OTHER

    def _next_paragraph(self, section: RawSection) -> Generator[tuple[RawParagraph, bool], None, None]:
        for item in section.items:
            if isinstance(item, RawParagraph):
                yield item, False
            elif isinstance(item, RawList):
                for list_item in item.all_items():
                    yield list_item, False
            elif isinstance(item, RawTable):
                for row in item.rows:
                    for cell in row.cells:
                        if cell.first:
                            for index, cell_item in enumerate(cell.items):
                                if isinstance(cell_item, RawParagraph):
                                    yield cell_item, index == 0


    def _add_elements(self, elements: list[str]) -> None:
        for element in elements:
            if element["short_name"] not in self.elements:
                self.elements[element["short_name"]] = element
            else:
                name = f"{element['short_name']} {self.repeat_index}"
                element["short_name"] = name
                self.elements[name] = element
                self.repeat_index += 1

    def _add_instructions(self, elements: list[str], instructions: list[str]) -> None:
        for element in elements:
            self.elements[element["short_name"]]["instructions"] += instructions

    def _extract_elements(
        self, section: RawSection, paragraph: RawParagraph
    ) -> list[str]:
        confirmed_elements = []
        potential_elements = find_elements(paragraph.text)
        for element in potential_elements:
            #print(f"POT ELEMENT: S={section.number}, E={element}")
            match = next(
                (
                    x
                    for x in paragraph.runs
                    if element in x.text and x.highlight == "GRAY_25 (16)"
                ),
                None,
            )
            if not match:
                #print("SECOND ATTEMPT")
                match = next(
                    (
                        x
                        for x in paragraph.runs
                        if element.startswith(x.text) and x.highlight == "GRAY_25 (16)"
                    ),
                    None,
                )
            if match:
                #print(f"MATCH: {element}")
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
        instructions = [
            x.text
            for x in paragraph.runs
            if x.color == "C00000" or x.style == "Instructional TExt"
        ]
        return instructions

    def _has_elements(self, para: RawParagraph) -> bool:
        return len(find_elements(para.text)) > 0
    
    def _has_instructions(self, para: RawParagraph) -> bool:
        return len(self._extract_instructions(para)) > 0
    
