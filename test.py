from raw_docx import RawDocx, RawDocument, RawParagraph, RawTable, RawList


raw_doc: RawDocument = RawDocx('data/test_data/example.docx').target_document
for section in raw_doc.sections:
  for item in section.items:
      if isinstance(item, RawParagraph):
          print(f"PARA: {section.number}, {item.text}")
      elif isinstance(item, RawList):
          for list_item in item.all_items():
            print(f"LIST: {section.number}, {list_item.text}")
      elif isinstance(item, RawTable):
          for row_index, row in enumerate(item.rows):
              for cell_index, cell in enumerate(row.cells):
                  if cell.first:
                      for index, cell_item in enumerate(cell.items):
                          if isinstance(cell_item, RawParagraph):
                              print(f"CELL PARA: {section.number}, [{row_index}, {cell_index}], {cell_item.text}")


