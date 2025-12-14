"""
Clinical Research Structured Template
Based on Lancet journal's 8-module structure
"""

from typing import Dict, List
import re


class ClinicalResearchTemplate:
    """Clinical research structured template (8 modules)"""

    # Module definitions
    MODULES = {
        'background': 'Background',
        'objective': 'Objective',
        'methods': 'Methods',
        'participants': 'Participants',
        'intervention': 'Intervention',
        'outcomes': 'Outcomes',
        'results': 'Results',
        'conclusion': 'Conclusion'
    }

    def extract(self, text: str, metadata: Dict = None) -> Dict:
        """
        Extract structured information from clinical research text

        Args:
            text: Full text or abstract of the paper
            metadata: Paper metadata

        Returns:
            Dictionary containing 8-module structured information
        """
        text_lower = text.lower()

        return {
            'paper_type': 'clinical_research',
            'modules': {
                'background': self._extract_background(text, text_lower),
                'objective': self._extract_objective(text, text_lower),
                'methods': self._extract_methods(text, text_lower),
                'participants': self._extract_participants(text, text_lower),
                'intervention': self._extract_intervention(text, text_lower),
                'outcomes': self._extract_outcomes(text, text_lower),
                'results': self._extract_results(text, text_lower),
                'conclusion': self._extract_conclusion(text, text_lower)
            },
            'metadata': metadata or {}
        }

    def _extract_background(self, text: str, text_lower: str) -> str:
        """Extract background"""
        patterns = [
            r'background[:\s]*(.*?)(?=\n\n|\. [A-Z]|\.objective|\. methods)',
            r'introduction[:\s]*(.*?)(?=\n\n|\. [A-Z]|\.objective)',
            r'background[:\s]*(.*?)(?=\n\n|objective)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]  # Limit length

        # Fallback: take first 200 characters
        return text[:200].strip() + "..."

    def _extract_objective(self, text: str, text_lower: str) -> str:
        """Extract objective"""
        patterns = [
            r'objective[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. methods|\.participants)',
            r'aim[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'objective[:\s]*(.*?)(?=\n\n|methods)',
            r'to (?:investigate|evaluate|assess|determine) (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:300]

        return "Objective not clearly stated"

    def _extract_methods(self, text: str, text_lower: str) -> str:
        """Extract methods"""
        patterns = [
            r'methods[:\s]*(.*?)(?=\n\n|\. [A-Z]|\.participants|\. intervention)',
            r'methodology[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'研究方法[:\s]*(.*?)(?=\n\n|participants)',
            r'(?:we conducted|this was) (.*?)(?:study|trial)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        return "Methods not clearly stated"

    def _extract_participants(self, text: str, text_lower: str) -> str:
        """Extract participants"""
        patterns = [
            r'participants[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. intervention|\. outcomes)',
            r'study population[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'participants[:\s]*(.*?)(?=\n\n|intervention)',
            r'(?:patients|participants) (?:with|aged|n =) (.*?)(?=\.|,|\n)',
            r'(\d+) patients? (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(0).strip()[:400]

        return "Participants information not clearly stated"

    def _extract_intervention(self, text: str, text_lower: str) -> str:
        """Extract intervention"""
        patterns = [
            r'intervention[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. outcomes|\. results)',
            r'treatment[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. outcomes)',
            r'intervention[:\s]*(.*?)(?=\n\n|outcomes)',
            r'(?:treatment|intervention) (?:with|using|consisted of) (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:400]

        return "Intervention not clearly stated"

    def _extract_outcomes(self, text: str, text_lower: str) -> str:
        """Extract outcomes"""
        patterns = [
            r'outcomes[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. results|\. conclusion)',
            r'primary outcome[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'outcomes[:\s]*(.*?)(?=\n\n|results)',
            r'(?:primary|main) (?:outcome|endpoint) (?:was|were) (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:400]

        return "Outcomes not clearly stated"

    def _extract_results(self, text: str, text_lower: str) -> str:
        """Extract results"""
        patterns = [
            r'results[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. conclusion|\. interpretation)',
            r'results[:\s]*(.*?)(?=\n\n|结论)',
            r'(?:we found|results show|showed) (.*?)(?=\.|,|\n)',
            r'(p\s*[<=>]\s*0\.\d+.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                result = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
                return result.strip()[:600]

        return "Results not clearly stated"

    def _extract_conclusion(self, text: str, text_lower: str) -> str:
        """Extract conclusion"""
        patterns = [
            r'conclusion[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. interpretation|$)',
            r'interpretation[:\s]*(.*?)(?=\n\n|\. [A-Z]|$)',
            r'结论[:\s]*(.*?)(?=\n\n|$)',
            r'(?:in conclusion|these findings) (.*?)(?=\.|,|\n|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:400]

        return "Conclusion not clearly stated"
