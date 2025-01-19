import json
from m11_template.m11_template import M11Template
from m11_template.m11_technical import M11Technical

#template = M11Template(filepath="data/input_data/m11-template-spec.docx")
#template.process()
technical = M11Technical(filepath="data/input_data/m11-technical-spec.docx")
technical.process()

#with open("data/output_data/m11.json", "w") as f:
#    json.dump(technical.document, f, indent=4)
with open("data/output_data/technical_elements.json", "w") as f:
    json.dump(technical.elements, f, indent=4)
