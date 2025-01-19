import re
import yaml
from pathlib import Path
from raw_docx import RawDocx, RawDocument, RawParagraph, RawTable, RawSection, RawTableRow


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
                        data_element = self._extract_data_element(section_item)
                        if data_element:
                            self.elements[data_element["name"]] = data_element
                            if index + 1 < len(section.items):
                                next_index = index + 1
                                while next_index < len(section.items):
                                    next_item = section.items[next_index]
                                    if isinstance(next_item, RawTable):
                                        if self._is_ncit_table(next_item):
                                            ncit_element = self._extract_ncit_element(next_item)
                                            if ncit_element:
                                                self.elements[data_element["name"]]["ct"] = ncit_element
                                        break
                                    next_index += 1
                    elif self._is_ncit_table(section_item):
                        #print(f"NCI THESAURUS TABLE:")
                        pass
                    else:
                        #print(f"TABLE: Other Type")
                        pass

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

    def _extract_data_element(self, table: RawTable) -> dict:
        """
        Extract the data element from the table.
        """
        data_element = None
        if len(table.rows) >= 10:
            data_element = {
                "name": self._clean_element_name(self._row_cell_text(table.rows[0], 1)),
                "data_type": self._row_cell_text(table.rows[1], 1),
                "definition": self._row_cell_text(table.rows[3], 1),
                "guidance": self._row_cell_text(table.rows[4], 1),
                "conformance": self._row_cell_text(table.rows[5], 1),
                "cardinality": self._row_cell_text(table.rows[6], 1),
                "relationship": self._row_cell_text(table.rows[7], 1),
                "value": self._row_cell_text(table.rows[8], 1),
                "business_rules": self._row_cell_text(table.rows[9], 1),
                "repeating": self._row_cell_text(table.rows[10], 1),
                "ct": []
            }
        return data_element

    def _extract_ncit_element(self, table: RawTable) -> dict:
        """
        Extract the NCI Thesaurus element from the table.
        """
        ncit_element = []
        for row in table.rows[1:]:
            ncit_element.append({
                "ncit_code": row.cells[0].text(),
                "preferred_term": row.cells[1].text(),
                "definition": row.cells[2].text()
            })
        return ncit_element

    def _is_data_element_table(self, table: RawTable) -> bool:
        """
        Check if the table is a data element table.
        """
        if len(table.rows) > 3:
            row_1 = table.rows[0]
            row_3 = table.rows[2]
            print(f"ROW 1: {self._row_cell_text(row_1, 0)} -> {self._row_cell_text(row_1, 1)}")
            if self._row_cell_text(row_1, 0).startswith("Term (Variable)") and self._row_cell_text(row_3, 1) in ["D", "V"]:
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

    def _clean_element_name(self, element_name: str) -> str:
        """
        Clean the element name. Remove any non-alphanumeric characters.
        """
        return re.sub(r'[^a-zA-Z0-9 ]', '', element_name)
