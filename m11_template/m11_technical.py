import re
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
            for section_item in section.items:
                if isinstance(section_item, RawParagraph):
                    print(f"PARAGRAPH: {section_item.text}")
                elif isinstance(section_item, RawTable):
                    if self._is_data_element_table(section_item):
                        data_element = self._extract_data_element(section_item)
                        if data_element:
                            self.elements[data_element["name"]] = data_element
                    elif self._is_ncit_table(section_item):
                        print(f"NCI THESAURUS TABLE:")
                    else:
                        print(f"TABLE: Other Type")


    def _extract_data_element(self, table: RawTable) -> dict:
        """
        Extract the data element from the table.
        """
        data_element = None
        if len(table.rows) >= 10:
            data_element = {
                "name": self._row_cell_text(table.rows[0], 1),
                "data_type": self._row_cell_text(table.rows[1], 1),
                "definition": self._row_cell_text(table.rows[3], 1),
                "guidance": self._row_cell_text(table.rows[4], 1),
                "conformance": self._row_cell_text(table.rows[5], 1),
                "cardinality": self._row_cell_text(table.rows[6], 1),
                "relationship": self._row_cell_text(table.rows[7], 1),
                "value": self._row_cell_text(table.rows[8], 1),
                "business_rules": self._row_cell_text(table.rows[9], 1),
                "repeating": self._row_cell_text(table.rows[10], 1),
            }
        return data_element

    def _is_data_element_table(self, table: RawTable) -> bool:
        """
        Check if the table is a data element table.
        """
        if len(table.rows) > 3:
            row_1 = table.rows[0]
            row_3 = table.rows[2]
            if self._row_cell_text(row_1, 0).startswith("Term (Variable)") and self._row_cell_text(row_3, 1) == "D":
                return True
        return False

    def _is_ncit_table(self, table: RawTable) -> bool:
        """
        Check if the table is a NCI Thesaurus table.
        """
        if len(table.rows) > 1:
            row_1 = table.rows[0]
            if self._row_cell_text(row_1, 0).startswith("NCI C-Code"):
                return True
        return False

    def _row_cell_text(self, row: RawTableRow, cell_index: int) -> str:
        if len(row.cells) > cell_index:
            cell = row.cells[cell_index]
            if cell.is_text():
                return cell.text()
        return ""
