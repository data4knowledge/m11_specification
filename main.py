import json
from m11_template.m11_template import M11Template
from m11_template.m11_technical import M11Technical
from itertools import zip_longest

version = "2025-02-03"
template = M11Template(filepath=f"m11_versions/{version}/specification/m11-template-spec.docx")
template.process()
template.rename_elements(filepath=f"m11_versions/{version}/fix_data/template_renames.yaml")
template.insert_elements(filepath=f"m11_versions/{version}/fix_data/template_inserts.yaml")
template.delete_elements(filepath=f"m11_versions/{version}/fix_data/template_deletes.yaml")
template.order_elements()
technical = M11Technical(filepath=f"m11_versions/{version}/specification/m11-technical-spec.docx")
technical.process()
technical.rename_elements(filepath=f"m11_versions/{version}/fix_data/technical_renames.yaml")
technical.insert_elements(filepath=f"m11_versions/{version}/fix_data/technical_inserts.yaml")
technical.delete_elements(filepath=f"m11_versions/{version}/fix_data/technical_deletes.yaml")

with open(f"m11_versions/{version}/output_data/template_document.json", "w") as f:
    json.dump(template.document, f, indent=4)
with open(f"m11_versions/{version}/output_data/template_elements.json", "w") as f:
    json.dump(template.elements, f, indent=4)
with open(f"m11_versions/{version}/output_data/template_sections.json", "w") as f:
    json.dump(template.sections, f, indent=4)
with open(f"m11_versions/{version}/output_data/technical_document.json", "w") as f:
    json.dump(technical.document, f, indent=4)
with open(f"m11_versions/{version}/output_data/technical_elements.json", "w") as f:
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

# with open("data/input_data/usdm/m11_mapping.yaml", "r") as f:
#     usdm = yaml.load(f, Loader=yaml.FullLoader)

# not_mapped = {}
# for key, value in merged.items():
#     if key in usdm:
#         merged[key]['usdm'] = usdm[key]
#     else:
#         not_mapped[key] = key

with open(f"m11_versions/{version}/output_data/merged_elements.json", "w") as f:
    json.dump(merged, f, indent=4)
with open(f"m11_versions/{version}/output_data/mismatched_elements.json", "w") as f:
    json.dump(missing, f, indent=4)
# with open("output_data/not_mapped_to_usdm_elements.json", "w") as f:
#     json.dump(not_mapped, f, indent=4)

res = list(zip_longest(missing['template'].keys(), missing['technical'].keys()))
#print(f"RES: {res}")
text = "<table><tr><th>Template</th><th>Technical</th></tr>"
blank1 = {'section_number': '', 'short_name': ''}
blank2 = {'relationship': '', 'name': ''}
for result in res:
 
    temp = template.elements[result[0]] if result[0] else blank1
    tech = technical.elements[result[1]] if result[1] else blank2
    temp_text = f"{temp['section_number']}: {temp['short_name']}"
    tech_text = f"{tech['relationship']}: {tech['name']}"
    text += f"<tr><td>{temp_text}</td><td>{tech_text}</td></tr>"
text += "</table>"
with open(f"m11_versions/{version}/output_data/mismatched_elements.html", "w") as f:
    f.write(text)
