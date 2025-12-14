"""
Paper type classifier tests
"""

import pytest
from modules.paper_classifier import PaperClassifier


class TestPaperClassifier:
    """Paper classifier test class"""

    @pytest.fixture
    def classifier(self):
        """Create classifier instance"""
        return PaperClassifier()

    def test_clinical_research_classification(self, classifier):
        """Test clinical research classification"""
        clinical_text = """
        Background: This randomized controlled trial aims to evaluate the efficacy
        of a new treatment in patients with diabetes. Methods: We conducted a
        prospective cohort study with 200 patients. The intervention group received
        the new drug, while the control group received placebo. The primary outcome
        was change in HbA1c levels. Results: The treatment group showed significant
        improvement (p < 0.001). Conclusion: The new treatment is effective.
        """
        paper_type, confidence = classifier.classify(clinical_text)
        assert paper_type == 'clinical_research'
        assert confidence > 0.5

    def test_case_report_classification(self, classifier):
        """Test case report classification"""
        case_text = """
        Case Report: We report a 65-year-old male patient who presented with
        chest pain and shortness of breath. Clinical examination revealed
        irregular heartbeat. The patient was diagnosed with atrial fibrillation
        based on ECG findings. Treatment with anticoagulation therapy was initiated.
        Follow-up showed good recovery.
        """
        paper_type, confidence = classifier.classify(case_text)
        assert paper_type == 'case_report'
        assert confidence > 0.5

    def test_basic_research_classification(self, classifier):
        """Test basic research classification"""
        basic_text = """
        Background: The molecular mechanism of gene regulation remains unclear.
        Methods: We performed cell culture experiments and Western blot analysis
        to examine protein expression. Results: Gene expression was significantly
        increased in treated cells (p < 0.05). Conclusion: The treatment activates
        the signaling pathway through protein upregulation.
        """
        paper_type, confidence = classifier.classify(basic_text)
        assert paper_type == 'basic_research'
        assert confidence > 0.5

    def test_get_classification_details(self, classifier):
        """Test get classification details"""
        text = "This randomized controlled trial included 100 patients..."
        details = classifier.get_classification_details(text)

        assert 'type' in details
        assert 'confidence' in details
        assert 'scores' in details
        assert 'type_description' in details
        assert details['type'] in ['clinical_research', 'case_report', 'basic_research']
