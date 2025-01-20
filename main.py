import json
import yaml
from m11_template.m11_template import M11Template
from m11_template.m11_technical import M11Technical
from tabulate import tabulate
from itertools import zip_longest


template = M11Template(filepath="data/input_data/m11/m11-template-spec.docx")
template.process()
template.rename_elements(filepath="data/input_data/m11/template_renames.yaml")
technical = M11Technical(filepath="data/input_data/m11/m11-technical-spec.docx")
technical.process()
technical.rename_elements(filepath="data/input_data/m11/technical_renames.yaml")

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
        #print(f"MISSING TEMPLATE: {key}")
for key, value in technical.elements.items():
    if key not in template.elements:
        missing['technical'][key] = value
        #print(f"MISSING TECHNICAL: {key}")

with open("data/input_data/usdm/m11_mapping.yaml", "r") as f:
    usdm = yaml.load(f, Loader=yaml.FullLoader)

for key, value in merged.items():
    if key in usdm:
        merged[key]['usdm'] = usdm[key]

with open("data/output_data/merged_elements.json", "w") as f:
    json.dump(merged, f, indent=4)
with open("data/output_data/mismatched_elements.json", "w") as f:
    json.dump(missing, f, indent=4)

res = zip_longest(missing['template'].keys(), missing['technical'].keys())
print("\n\nResults: Unmatched Items\n\n")
print(tabulate(res, headers=['Template', 'Technical'], tablefmt="github"))
