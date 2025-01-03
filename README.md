# M11 Specification Processor

A Python package for processing ICH M11 clinical trial protocol documents. This package takes two PDF documents as input:
1. Template Specification - Contains the template structure with required and optional data elements
2. Technical Specification - Contains detailed information about data elements

## Features

- Processes Template Specification PDF with color-coded text interpretation:
  - Red text: informational text
  - Black text: template specification
  - Black text with grey shading in brackets: required data elements
  - Blue text with grey shading in brackets: optional data elements
- Extracts data element definitions from Technical Specification tables
- Relates data elements between both documents
- Outputs a structured JSON containing:
  - List of sections with numbers and titles
  - List of all data elements
  - Mapping between data elements and their parent sections

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from m11_specification import M11Processor

# Initialize processor with paths to both PDFs
processor = M11Processor(
    template_spec_path="path/to/template_spec.pdf",
    technical_spec_path="path/to/technical_spec.pdf"
)

# Process the documents and get the results
results = processor.process()

# Or save directly to JSON file
processor.save_to_json("output.json")
```

## Output Format

The output JSON has the following structure:

```json
{
  "sections": [
    {
      "section_number": "1.1",
      "title": "Section Title"
    }
  ],
  "data_elements": [
    {
      "element_name": "ElementName",
      "required": true,
      "optional": false,
      "technical_spec": {
        "definition": "Element definition",
        "conformance": "Conformance info",
        "data_type": "Data type info"
      }
    }
  ],
  "element_section_mapping": [
    {
      "element_name": "ElementName",
      "section_number": "1.1"
    }
  ]
}
```

## Requirements

- Python 3.8 or higher
- PyPDF2
- pdfplumber
- python-json-logger
