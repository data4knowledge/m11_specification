import yaml
import re
from pathlib import Path
from raw_docx import RawDocx, RawDocument, RawParagraph, RawTable, RawTableRow
from m11_template.m11_utility import clean_element_name, find_elements

class M11Technical:
    def __init__(self, filepath: str):
        self.document = None
        self.elements = {}
        self.filepath = Path(filepath)
        self.repeat_index = 1
        if not self.filepath.exists():
            raise FileNotFoundError(
                f"M11 Technical Document not found: {filepath}"
            )

    def process(self) -> None:
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
        with open(filepath, "r") as f:
            insert_dict = yaml.safe_load(f)
        for key, value in insert_dict.items():
            if key in self.elements:
                self.elements.pop(key)
            else:
                print(f"Technical delete not required: {key}")

    def _extract_data_elements(self, table: RawTable) -> list[dict]:
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
                "definition": self._decode_definition(table.rows[3], 1),
                "guidance": self._row_cell_text(table.rows[4], 1).strip(),
                "conformance": self._row_cell_text(table.rows[5], 1).strip(),
                "cardinality": self._row_cell_text(table.rows[6], 1).strip(),
                "relationship": self._row_cell_text(table.rows[7], 1).strip(),
                "value": self._row_cell_text(table.rows[8], 1).strip(),
                "business_rules": self._decode_business_rules(table.rows[9], 1),
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
        ncit_element = []
        for row in table.rows[1:]:
            ncit_element.append({
                "ncit_code": row.cells[0].text().strip(),
                "preferred_term": row.cells[1].text().strip(),
                "definition": row.cells[2].text().strip()
            })
        return ncit_element

    def _is_data_element_table(self, table: RawTable) -> bool:
        if len(table.rows) > 3:
            row_1 = table.rows[0]
            row_3 = table.rows[2]
            item_text = self._row_cell_text(row_1, 0).strip()
            item_name = self._row_cell_text(row_1, 1).strip()
            item_type = self._row_cell_text(row_3, 1).strip()
            #print(f"ROWS: {item_text}={item_name}, Type={item_type}")
            if item_text.startswith("Term (Variable)"):
                if item_type in ["D", "V", "V or D", "D, V"]:
                    #print(f"TRUE")
                    return True
                if item_name.startswith("[") and item_name.endswith("]") and item_type == "H":
                    #print(f"TRUE")
                    return True
        return False

    def _is_ncit_table(self, table: RawTable) -> bool:
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

    def _decode_business_rules(self, row: RawTableRow, cell_index: int) -> dict:
        result = {
            'value_allowed': '',
            'relationship': '',
            'concept': '',
            'other': ''
        }
        if len(row.cells) > cell_index:
            cell = row.cells[cell_index]
            for item in cell.items:
                if isinstance(item , RawParagraph):
                    if item.text.startswith("Value Allowed:"):
                        result['value_allowed'] = item.text.replace("Value Allowed:", "").strip()
                    elif item.text.startswith("Relationship:"):
                        result['relationship'] = item.text.replace("Relationship:", "").strip()
                    elif item.text.startswith("Concept:"):
                        result['concept'] = item.text.replace("Concept:", "").strip()
                    else:
                        result['other'] = item.text.strip()
        return result
    
    def _decode_definition(self, row: RawTableRow, cell_index: int) -> dict:
        result = []
        if len(row.cells) > cell_index:
            cell = row.cells[cell_index]
            if cell.is_text():
                lines = cell.text().split("\n")
                state = "OUTSIDE"
                for line in lines:
                    print(f"LINE: {line}, {state}")
                    if line.startswith("For review purpose, see definition of the controlled terminology below"):
                        pass
                    elif self._is_c_code(line):
                        state = "INSIDE"
                        c_code = line
                    elif state == "INSIDE":
                        if len(line.strip()) > 0:
                            result.append({'c_code': c_code, 'definition': line.strip()})
                        state = "OUTSIDE"
        return result
    
    def _is_c_code(self, text: str) -> bool:
        pattern = r'C(?:NEW|\d+)'
        match = re.search(pattern, text)
        print(f"MATCH: {'TRUE' if match else 'FALSE'}")
        return True if match else False