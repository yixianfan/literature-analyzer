"""
Information Extraction Module
Coordinates paper classification and structured extraction
"""

from typing import Dict
from .paper_classifier import PaperClassifier
from templates.clinical_template import ClinicalResearchTemplate
from templates.case_template import CaseReportTemplate
from templates.basic_template import BasicResearchTemplate


class InfoExtractor:
    """Information extractor"""

    def __init__(self):
        """Initialize the extractor"""
        self.classifier = PaperClassifier()
        self.templates = {
            'clinical_research': ClinicalResearchTemplate(),
            'case_report': CaseReportTemplate(),
            'basic_research': BasicResearchTemplate()
        }

    def extract(self, text: str, metadata: Dict = None) -> Dict:
        """
        Extract paper information

        Args:
            text: Paper text
            metadata: Paper metadata

        Returns:
            Dictionary containing detailed information

        Raises:
            ValueError: Unrecognized paper type
        """
        # Classify paper
        classification = self.classifier.get_classification_details(text)
        paper_type = classification['type']
        confidence = classification['confidence']

        # Get template
        if paper_type not in self.templates:
            raise ValueError(f"Unsupported paper type: {paper_type}")

        template = self.templates[paper_type]

        # Extract structured information
        extracted_info = template.extract(text, metadata)

        # Add classification information
        extracted_info['classification'] = {
            'type': paper_type,
            'type_description': classification['type_description'],
            'confidence': confidence
        }

        return extracted_info

    def get_paper_type_description(self, paper_type: str) -> str:
        """
        Get paper type description

        Args:
            paper_type: Paper type

        Returns:
            Type description
        """
        descriptions = {
            'clinical_research': 'Clinical Research',
            'case_report': 'Case Report',
            'basic_research': 'Basic Research'
        }
        return descriptions.get(paper_type, 'Unknown type')

    def get_template_modules(self, paper_type: str) -> Dict:
        """
        Get template module information

        Args:
            paper_type: Paper type

        Returns:
            Module information dictionary
        """
        if paper_type not in self.templates:
            return {}

        template = self.templates[paper_type]
        return template.MODULES
