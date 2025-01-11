import json
from m11_template.m11_template import M11Template

template = M11Template(filepath="data/input_data/m11-template-spec.docx")
results = template.process()
with open("data/output_data/m11.json", 'w') as f:
    json.dump(results, f, indent=4)

