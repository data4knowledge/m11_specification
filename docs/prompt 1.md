# Prompt

1. Write a python package that takes two PDF documents as the inputs.
2. The documents can be stored locally and referenced by full path manes
3. One document is the specification of a template, the Template Specification, for clinical trial protocol documents, see https://www.ema.europa.eu/en/documents/scientific-guideline/ich-m11-template-step-2b_en.pdf for an example
4. The second document, the Technical Specification, contains additional information on the fields to be contained within the protocol document, see https://www.ema.europa.eu/en/documents/scientific-guideline/ich-m11-technical-specification-step-2b_en.pdf for an example
5. Process the Template Specification using the following rules:
	1. All red text is informational text
	2. Black text is part of the template specification
	3. Required data elements are indicated in Black Text with grey shading within square brackets
	4. Optional data elements are indicated in Blue text with grey shading within square brackets
7. Process the Technical Specification as follows:
	1. Extract all the data element definitions from each table
	2. Relate the data element definitions to the template specification via the Term (Varaible) names
8. The output should be a JSON structure containing:
	1. a list of sections including section number and title
	2. a list of all data elements
	3. A list relating each data element to their parent section

# Prompt Response

I've created a complete Python package for processing ICH M11 clinical trial protocol documents. Here's a summary of what I've created:

Package Structure:
- m11_specification/ - Main package directory
- processor.py - Core processing logic
- init.py - Package initialization
- setup.py - Package setup and dependencies
- requirements.txt - Required Python packages
- Updated README.md - Comprehensive documentation
Key Features:
- Processes both Template and Technical Specifications
- Handles color-coded text interpretation
- Extracts section structure and data elements
- Creates relationships between elements and sections
- Outputs structured JSON data
- Includes logging with JSON formatting
- Error handling for file operations
Dependencies:
- PyPDF2 - PDF processing
- pdfplumber - Advanced PDF text extraction with color information
python-json-logger - JSON formatted logging

To use the package, you would need to:

Install the requirements:
pip install -r requirements.txt

Use the package in your code:

```
from m11_specification import M11Processor

processor = M11Processor(
    template_spec_path="/path/to/template.pdf",
    technical_spec_path="/path/to/technical.pdf"
)
results = processor.process()
````

# Or save to JSON

```
processor.save_to_json("output.json")
```

# Install And Running The Code

```Shell
Last login: Thu Jan  2 19:52:44 on console
daveih@dih-m1-mini ~ % cd Documents/python/m11_specification 
daveih@dih-m1-mini m11_specification % python3 -m venv .venv
daveih@dih-m1-mini m11_specification % source .venv/bin/activate
(.venv) daveih@dih-m1-mini m11_specification % pip install -r requirements.txt 
Collecting PyPDF2>=3.0.0
  Downloading pypdf2-3.0.1-py3-none-any.whl (232 kB)
     |████████████████████████████████| 232 kB 4.3 MB/s 
Collecting pdfplumber>=0.10.2
  Downloading pdfplumber-0.11.5-py3-none-any.whl (59 kB)
     |████████████████████████████████| 59 kB 10.2 MB/s 
Collecting python-json-logger>=2.0.7
  Downloading python_json_logger-3.2.1-py3-none-any.whl (14 kB)
Collecting pypdfium2>=4.18.0
  Downloading pypdfium2-4.30.1-py3-none-macosx_11_0_arm64.whl (2.8 MB)
     |████████████████████████████████| 2.8 MB 10.2 MB/s 
Collecting pdfminer.six==20231228
  Downloading pdfminer.six-20231228-py3-none-any.whl (5.6 MB)
     |████████████████████████████████| 5.6 MB 10.7 MB/s 
Collecting Pillow>=9.1
  Downloading pillow-11.1.0-cp310-cp310-macosx_11_0_arm64.whl (3.1 MB)
     |████████████████████████████████| 3.1 MB 10.1 MB/s 
Collecting charset-normalizer>=2.0.0
  Using cached charset_normalizer-3.4.1-cp310-cp310-macosx_10_9_universal2.whl (198 kB)
Collecting cryptography>=36.0.0
  Using cached cryptography-44.0.0-cp39-abi3-macosx_10_9_universal2.whl (6.5 MB)
Collecting cffi>=1.12
  Using cached cffi-1.17.1-cp310-cp310-macosx_11_0_arm64.whl (178 kB)
Collecting pycparser
  Using cached pycparser-2.22-py3-none-any.whl (117 kB)
Installing collected packages: pycparser, cffi, cryptography, charset-normalizer, pypdfium2, Pillow, pdfminer.six, python-json-logger, PyPDF2, pdfplumber
Successfully installed Pillow-11.1.0 PyPDF2-3.0.1 cffi-1.17.1 charset-normalizer-3.4.1 cryptography-44.0.0 pdfminer.six-20231228 pdfplumber-0.11.5 pycparser-2.22 pypdfium2-4.30.1 python-json-logger-3.2.1
WARNING: You are using pip version 21.2.4; however, version 24.3.1 is available.
You should consider upgrading via the '/Users/daveih/Documents/python/m11_specification/.venv/bin/python3 -m pip install --upgrade pip' command.
(.venv) daveih@dih-m1-mini m11_specification % python main.py
{"message": "Starting template specification processing"}
{"message": "Starting technical specification processing"}
{"message": "Results saved to data/input_data/m11.json"}
(.venv) daveih@dih-m1-mini m11_specification % 
```