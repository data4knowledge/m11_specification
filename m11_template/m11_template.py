from pathlib import Path
from raw_docx import RawDocx, RawDocument, RawParagraph, RawTable

class M11Template:

    def __init__(self, filepath: str):
        """
        Initialize the M11 processor with paths to both specification documents.

        Args:
            template_spec_path (str): Path to the Template Specification PDF
            technical_spec_path (str): Path to the Technical Specification PDF
        """
        self.result = None
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(
                f"Template specification file not found: {filepath}"
            )

    def process(self):
        raw_doc: RawDocument = RawDocx(self.filepath).target_document
        self.result = raw_doc.to_dict()
        for section in raw_doc.sections:
            for item in section.items:
                if isinstance(item, RawParagraph):
                    print(f"PARA: {item.runs}")
                elif isinstance(item, RawTable):
                    pass
        return self.result
    
    # def _extract_elements(self, data: list[dict]):
    #     index = 0
    #     more = False
    #     while not more and index < len(data):
    #         run = data[index]
    #         if not run["text"]:
    #             run["keep"] = False
    #             more = True
    #         elif (index < len(data) - 1) and run["text"][-1] in ["<", "[", "{"]:
    #             run["text"] = run["text"] + data[index + 1]["text"]
    #             run["style"] = (
    #                 data[index + 1]["style"]
    #                 if data[index + 1]["style"] == "CPT_Variable"
    #                 else run["style"]
    #             )
    #             data[index + 1]["keep"] = False
    #             more = True
    #         elif index > 0 and run["text"][0] in [">", "]", "}"]:
    #             data[index - 1]["text"] = data[index - 1]["text"] + run["text"]
    #             data[index - 1]["style"] = (
    #                 run["style"]
    #                 if run["style"] == "CPT_Variable"
    #                 else data[index - 1]["style"]
    #             )
    #             run["keep"] = False
    #             more = True
    #         elif index > 0 and run["text"]:
    #             start_char = run["text"][0]
    #             end_char = run["text"][-1]
    #             if (
    #                 (end_char == ">" and start_char != "<")
    #                 or (end_char == "]" and start_char != "[")
    #                 or (end_char == "}" and start_char != "{")
    #             ):
    #                 data[index - 1]["text"] = data[index - 1]["text"] + run["text"]
    #                 data[index - 1]["style"] = (
    #                     run["style"]
    #                     if run["style"] == "CPT_Variable"
    #                     else data[index - 1]["style"]
    #                 )
    #                 run["keep"] = False
    #                 more = True
    #         index += 1
    #     new_data = [x for x in data if x["keep"]]
    #     if more:
    #         new_data = self._extract_elements(new_data)
    #     return new_data
