"""
Paper Type Classification Module
Automatically identifies paper types: Clinical Research, Case Reports, Basic Research
"""

import re
from typing import Dict, List, Tuple


class PaperClassifier:
    """Paper type classifier"""

    # Clinical research keywords
    CLINICAL_KEYWORDS = {
        'study_design': [
            'randomized controlled trial', 'RCT', 'cohort', 'case-control',
            'cross-sectional', 'prospective', 'retrospective', 'clinical trial',
            'randomized controlled trial', 'cohort study', 'case-control study', 'cross-sectional study'
        ],
        'participants': [
            'patients', 'participants', 'subjects', 'n =', 'patients with',
            'patients', 'subjects', 'study subjects'
        ],
        'intervention': [
            'treatment', 'intervention', 'therapy', 'drug', 'medication',
            'surgery', 'procedure', 'treatment', 'intervention', 'drug', 'surgery'
        ],
        'outcomes': [
            'outcome', 'endpoint', 'efficacy', 'safety', 'effectiveness',
            'outcome', 'endpoint', 'efficacy', 'safety'
        ],
        'statistics': [
            'p-value', 'confidence interval', 'odds ratio', 'hazard ratio',
            '95% CI', 'P <', 'P =', 'p<', 'confidence interval', 'odds ratio'
        ]
    }

    # Case report keywords
    CASE_KEYWORDS = {
        'case_report': [
            'case report', 'case presentation', 'case study', 'case report',
            'case study', 'case report'
        ],
        'patient_info': [
            'patient was', 'patient presented with', 'patient developed',
            'patient', 'years old', 'year old', 'male', 'female'
        ],
        'clinical_features': [
            'presented with', 'complained of', 'diagnosed with',
            'presented with', 'chief complaint', 'diagnosis'
        ],
        'diagnosis': [
            'diagnosis', 'diagnosed', 'confirmed by',
            'diagnosis', 'diagnosed', 'confirmed'
        ],
        'treatment_outcome': [
            'treatment', 'therapy', 'outcome', 'follow-up',
            'treatment', 'efficacy', 'outcome', 'follow-up'
        ]
    }

    # Basic research keywords
    BASIC_KEYWORDS = {
        'methods': [
            'methodology', 'experiment', 'cell culture', 'mice', 'rats',
            'methods', 'experiment', 'cell culture', 'mice', 'rats'
        ],
        'molecular': [
            'gene', 'protein', 'expression', 'pathway', 'mechanism',
            'gene', 'protein', 'expression', 'pathway', 'mechanism'
        ],
        'results_data': [
            'increased', 'decreased', 'significant', 'data show',
            'increased', 'decreased', 'significant', 'data show'
        ],
        'biological': [
            'biological', 'molecular', 'cellular', 'biochemical',
            'biological', 'molecular', 'cellular', 'biochemical'
        ]
    }

    def __init__(self):
        """Initialize the classifier"""
        self.clinical_patterns = self._compile_patterns(self.CLINICAL_KEYWORDS)
        self.case_patterns = self._compile_patterns(self.CASE_KEYWORDS)
        self.basic_patterns = self._compile_patterns(self.BASIC_KEYWORDS)

    def _compile_patterns(self, keywords_dict: Dict[str, List[str]]) -> Dict[str, List[re.Pattern]]:
        """Compile keywords into regular expressions"""
        patterns = {}
        for category, keywords in keywords_dict.items():
            patterns[category] = [
                re.compile(keyword, re.IGNORECASE) for keyword in keywords
            ]
        return patterns

    def classify(self, text: str) -> Tuple[str, float]:
        """
        Classify paper type

        Args:
            text: Paper text

        Returns:
            Tuple[paper type, confidence score]
        """
        # Calculate scores for each category
        clinical_score = self._calculate_score(text, self.clinical_patterns)
        case_score = self._calculate_score(text, self.case_patterns)
        basic_score = self._calculate_score(text, self.basic_patterns)

        # Calculate normalized scores
        scores = {
            'clinical_research': clinical_score,
            'case_report': case_score,
            'basic_research': basic_score
        }

        # Get highest score
        total_score = sum(scores.values())
        if total_score == 0:
            return 'basic_research', 0.5  # Default to basic research

        max_type = max(scores, key=scores.get)
        confidence = scores[max_type] / total_score

        return max_type, confidence

    def _calculate_score(self, text: str, patterns: Dict[str, List[re.Pattern]]) -> float:
        """Calculate text score"""
        score = 0.0
        text_lower = text.lower()

        for category, pattern_list in patterns.items():
            matches = sum(1 for pattern in pattern_list if pattern.search(text_lower))
            # Set weight based on category
            weight = self._get_category_weight(category)
            score += matches * weight

        return score

    def _get_category_weight(self, category: str) -> float:
        """Get category weight"""
        weights = {
            'study_design': 3.0,
            'participants': 2.5,
            'intervention': 2.5,
            'outcomes': 2.0,
            'statistics': 1.5,
            'case_report': 3.0,
            'patient_info': 2.5,
            'clinical_features': 2.0,
            'diagnosis': 2.5,
            'treatment_outcome': 2.0,
            'methods': 2.5,
            'molecular': 2.0,
            'results_data': 1.5,
            'biological': 2.0
        }
        return weights.get(category, 1.0)

    def get_classification_details(self, text: str) -> Dict:
        """
        Get detailed classification information

        Args:
            text: Paper text

        Returns:
            Dictionary containing detailed classification information
        """
        paper_type, confidence = self.classify(text)

        clinical_score = self._calculate_score(text, self.clinical_patterns)
        case_score = self._calculate_score(text, self.case_patterns)
        basic_score = self._calculate_score(text, self.basic_patterns)

        return {
            'type': paper_type,
            'confidence': confidence,
            'scores': {
                'clinical_research': clinical_score,
                'case_report': case_score,
                'basic_research': basic_score
            },
            'type_description': {
                'clinical_research': 'Clinical Research',
                'case_report': 'Case Report',
                'basic_research': 'Basic Research'
            }[paper_type]
        }
