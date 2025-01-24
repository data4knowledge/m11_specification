import yaml
from pathlib import Path
from raw_docx import RawDocx, RawDocument, RawParagraph, RawTable, RawSection, RawTableRow
from m11_template.m11_utility import clean_element_name, find_elements

class M11Technical:
    def __init__(self, filepath: str):
        """
        Initialize the M11 technical document processor.

        Args:
            filepath (str): Path to the M11 Technical Document
        """
        self.document = None
        self.elements = {}
        self.filepath = Path(filepath)
        self.repeat_index = 1
        if not self.filepath.exists():
            raise FileNotFoundError(
                f"M11 Technical Document not found: {filepath}"
            )

    def process(self) -> None:
        """
        Process the M11 Technical Document.
        """                                    
        raw_doc: RawDocument = RawDocx(self.filepath).target_document
        self.document = raw_doc.to_dict()
        for section in raw_doc.sections:
            for index, section_item in enumerate(section.items):
                if isinstance(section_item, RawParagraph):
                    #print(f"PARAGRAPH: {section_item.text}")
                    pass
                elif isinstance(section_item, RawTable):
                    if self._is_data_element_table(section_item):
                        data_elements = self._extract_data_elements(section_item)
                        if data_elements:
                            ct = self._extract_ct(section.items, index)
                            for data_element in data_elements:
                                data_element["ct"] = ct
                                self._add_element(data_element)
                    elif self._is_ncit_table(section_item):
                        #print(f"NCI THESAURUS TABLE:")
                        pass
                    else:
                        #print(f"TABLE: Other Type")
                        pass

    def _add_element(self, element: dict) -> None:
        if element["name"] not in self.elements:
            self.elements[element["name"]] = element
        else:
            name = f"{element['name']} {self.repeat_index}"
            element["name"] = name
            self.elements[name] = element
            self.repeat_index += 1

    def _extract_ct(self, items: list, index: int) -> list:
        if index + 1 < len(items):
            next_index = index + 1
            while next_index < len(items):
                next_item = items[next_index]
                if isinstance(next_item, RawTable):
                    if self._is_ncit_table(next_item):
                        return self._extract_ncit_element(next_item)
                    else:
                        break
                else:
                    next_index += 1
        return []
    
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
            else:
                print(f"Technical rename not required: {key}")

    def delete_elements(self, filepath: str) -> None:
        """
        Delete elements from the elements dictionary.
        """
        with open(filepath, "r") as f:
            insert_dict = yaml.safe_load(f)
        for key, value in insert_dict.items():
            if key in self.elements:
                self.elements.pop(key)
            else:
                print(f"Technical delete not required: {key}")

    def _extract_data_elements(self, table: RawTable) -> list[dict]:
        """
        Extract the data elements from the table.
        """
        result = []
        data_element = None
        if len(table.rows) >= 10:
            text = self._row_cell_text(table.rows[0], 1)
            data_elements = find_elements(text)
            #print(f"DATA ELEMENTS: {data_elements}")
            data_elements = [text] if not data_elements else data_elements
            template = {
                "name": "temp",
                "data_type": self._row_cell_text(table.rows[1], 1).strip(),
                "definition": self._row_cell_text(table.rows[3], 1).strip(),
                "guidance": self._row_cell_text(table.rows[4], 1).strip(),
                "conformance": self._row_cell_text(table.rows[5], 1).strip(),
                "cardinality": self._row_cell_text(table.rows[6], 1).strip(),
                "relationship": self._row_cell_text(table.rows[7], 1).strip(),
                "value": self._row_cell_text(table.rows[8], 1).strip(),
                "business_rules": self._row_cell_text(table.rows[9], 1).strip(),
                "repeating": self._row_cell_text(table.rows[10], 1).strip(),
                "ct": []
            }
            for data_element in data_elements:
                temp = dict(template)
                temp["name"] = clean_element_name(data_element)
                result.append(temp)
        #print(f"RESULT: {result}")
        return result

    def _extract_ncit_element(self, table: RawTable) -> dict:
        """
        Extract the NCI Thesaurus element from the table.
        """
        ncit_element = []
        for row in table.rows[1:]:
            ncit_element.append({
                "ncit_code": row.cells[0].text().strip(),
                "preferred_term": row.cells[1].text().strip(),
                "definition": row.cells[2].text().strip()
            })
        return ncit_element

    def _is_data_element_table(self, table: RawTable) -> bool:
        """
        Check if the table is a data element table.
        """
        if len(table.rows) > 3:
            row_1 = table.rows[0]
            row_3 = table.rows[2]
            #print(f"ROW 1: {self._row_cell_text(row_1, 0)} -> {self._row_cell_text(row_1, 1)}")
            #print(f"ROW 3: {self._row_cell_text(row_3, 0)} -> {self._row_cell_text(row_3, 1)}")
            if self._row_cell_text(row_1, 0).strip().startswith("Term (Variable)") and self._row_cell_text(row_3, 1).strip() in ["D", "V"]:
                #print(f"TRUE")
                return True
        return False

    def _is_ncit_table(self, table: RawTable) -> bool:
        """
        Check if the table is a NCI Thesaurus table.
        """
        if len(table.rows) > 1:
            row_1 = table.rows[0]
            #print(f"ROW 1: {self._row_cell_text(row_1, 0)}")
            if self._row_cell_text(row_1, 0).startswith("NCI C-Code"):
                return True
        return False

    def _row_cell_text(self, row: RawTableRow, cell_index: int) -> str:
        if len(row.cells) > cell_index:
            cell = row.cells[cell_index]
            if cell.is_text():
                return cell.text()
        return ""


