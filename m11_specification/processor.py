import json
import re
from typing import Dict, List, Optional, Tuple
import pdfplumber
from pathlib import Path
import logging
from pythonjsonlogger import jsonlogger

# Configure logging
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

class M11Processor:
    def __init__(self, template_spec_path: str, technical_spec_path: str):
        """
        Initialize the M11 processor with paths to both specification documents.
        
        Args:
            template_spec_path (str): Path to the Template Specification PDF
            technical_spec_path (str): Path to the Technical Specification PDF
        """
        self.template_spec_path = Path(template_spec_path)
        self.technical_spec_path = Path(technical_spec_path)
        self.sections = []
        self.data_elements = []
        self.element_section_mapping = []
        
        if not self.template_spec_path.exists():
            raise FileNotFoundError(f"Template specification file not found: {template_spec_path}")
        if not self.technical_spec_path.exists():
            raise FileNotFoundError(f"Technical specification file not found: {technical_spec_path}")

    def _extract_color_from_text(self, text_obj: Dict) -> str:
        """Extract color from PDF text object."""
        if 'non_stroking_color' in text_obj:
            color = text_obj['non_stroking_color']
            if color == (1, 0, 0):  # Red
                return 'red'
            elif color == (0, 0, 1):  # Blue
                return 'blue'
            return 'black'
        return 'black'

    def _is_section_header(self, text: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if text is a section header and extract section number and title.
        
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: (is_header, section_number, section_title)
        """
        pattern = r'^(\d+(?:\.\d+)*)\s+(.+)$'
        match = re.match(pattern, text.strip())
        if match:
            return True, match.group(1), match.group(2)
        return False, None, None

    def _extract_data_element(self, text: str, color: str) -> Optional[Dict]:
        """Extract data element from text if it matches the format."""
        pattern = r'\[(.*?)\]'
        match = re.search(pattern, text)
        if match:
            return {
                'element_name': match.group(1),
                'required': color == 'black',
                'optional': color == 'blue'
            }
        return None

    def process_template_specification(self):
        """Process the template specification PDF."""
        current_section = None
        
        with pdfplumber.open(self.template_spec_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(extra_attrs=['non_stroking_color'])
                
                for word in words:
                    text = word['text']
                    color = self._extract_color_from_text(word)
                    
                    # Check for section headers
                    is_header, section_num, section_title = self._is_section_header(text)
                    if is_header:
                        current_section = {
                            'section_number': section_num,
                            'title': section_title
                        }
                        self.sections.append(current_section)
                        continue
                    
                    # Process data elements
                    if color in ['black', 'blue']:
                        element = self._extract_data_element(text, color)
                        if element and current_section:
                            self.data_elements.append(element)
                            self.element_section_mapping.append({
                                'element_name': element['element_name'],
                                'section_number': current_section['section_number']
                            })

    def process_technical_specification(self):
        """Process the technical specification PDF to extract data element definitions."""
        with pdfplumber.open(self.technical_spec_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if not table or len(table) < 2:  # Skip empty or header-only tables
                        continue
                    
                    # Process table rows (skip header)
                    for row in table[1:]:
                        if not row or not any(row):  # Skip empty rows
                            continue
                        
                        # Assuming standard table format with Term (Variable) in first column
                        term = row[0] if row else None
                        if term:
                            # Update existing data element with technical specifications
                            for element in self.data_elements:
                                if element['element_name'] == term:
                                    element['technical_spec'] = {
                                        'definition': row[1] if len(row) > 1 else None,
                                        'conformance': row[2] if len(row) > 2 else None,
                                        'data_type': row[3] if len(row) > 3 else None
                                    }

    def process(self) -> Dict:
        """
        Process both specification documents and return structured data.
        
        Returns:
            Dict: Structured data containing sections, data elements, and mappings
        """
        logger.info("Starting template specification processing")
        self.process_template_specification()
        
        logger.info("Starting technical specification processing")
        self.process_technical_specification()
        
        return {
            'sections': self.sections,
            'data_elements': self.data_elements,
            'element_section_mapping': self.element_section_mapping
        }

    def save_to_json(self, output_path: str):
        """
        Process the specifications and save the results to a JSON file.
        
        Args:
            output_path (str): Path where the JSON output should be saved
        """
        result = self.process()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"Results saved to {output_path}")
