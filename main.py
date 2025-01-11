import json
from m11_template.m11_template import M11Template

template = M11Template(filepath="data/input_data/m11-template-spec.docx")
template.process()
with open("data/output_data/m11.json", "w") as f:
    json.dump(template.document, f, indent=4)
with open("data/output_data/elements.json", "w") as f:
    json.dump(template.elements, f, indent=4)
