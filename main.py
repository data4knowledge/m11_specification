import json
from m11_template.m11_template import M11Template
from m11_template.m11_technical import M11Technical

template = M11Template(filepath="data/input_data/m11-template-spec.docx")
template.process()
technical = M11Technical(filepath="data/input_data/m11-technical-spec.docx")
technical.process()

with open("data/output_data/template_document.json", "w") as f:
    json.dump(template.document, f, indent=4)
with open("data/output_data/template_elements.json", "w") as f:
    json.dump(template.elements, f, indent=4)
with open("data/output_data/technical_document.json", "w") as f:
    json.dump(technical.document, f, indent=4)#
with open("data/output_data/technical_elements.json", "w") as f:
    json.dump(technical.elements, f, indent=4)

merged = {}
missing = {'template': {}, 'technical': {}}
for key, value in template.elements.items():
    if key in technical.elements:
        merged[key] = {
            "template": value,
            "technical": technical.elements[key]
        }
    else:
        missing['template'][key] = value
        print(f"MISSING TEMPLATE: {key}")
for key, value in technical.elements.items():
    if key not in template.elements:
        missing['technical'][key] = value
        print(f"MISSING TECHNICAL: {key}")

with open("data/output_data/merged_elements.json", "w") as f:
    json.dump(merged, f, indent=4)
with open("data/output_data/mismatched_elements.json", "w") as f:
    json.dump(missing, f, indent=4)