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