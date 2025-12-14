"""
Structured template tests
"""

import pytest
from templates.clinical_template import ClinicalResearchTemplate
from templates.case_template import CaseReportTemplate
from templates.basic_template import BasicResearchTemplate


class TestClinicalResearchTemplate:
    """Clinical research template tests"""

    @pytest.fixture
    def template(self):
        return ClinicalResearchTemplate()

    def test_extract_clinical_research(self, template):
        """Test extract clinical research"""
        text = """
        Background: Diabetes treatment study.
        Objective: To evaluate new drug efficacy.
        Methods: RCT with 100 patients.
        Results: Significant improvement (p<0.001).
        Conclusion: Drug is effective.
        """
        result = template.extract(text)

        assert result['paper_type'] == 'clinical_research'
        assert 'background' in result['modules']
        assert 'objective' in result['modules']
        assert 'methods' in result['modules']
        assert 'results' in result['modules']
        assert 'conclusion' in result['modules']


class TestCaseReportTemplate:
    """Case report template tests"""

    @pytest.fixture
    def template(self):
        return CaseReportTemplate()

    def test_extract_case_report(self, template):
        """Test extract case report"""
        text = """
        Case Report: 65-year-old male with chest pain.
        Clinical Presentation: Patient presented with shortness of breath.
        Diagnosis: Atrial fibrillation confirmed by ECG.
        Treatment: Anticoagulation therapy initiated.
        Outcome: Good recovery at follow-up.
        """
        result = template.extract(text)

        assert result['paper_type'] == 'case_report'
        assert 'case_summary' in result['modules']
        assert 'clinical_presentation' in result['modules']
        assert 'diagnosis' in result['modules']
        assert 'treatment' in result['modules']
        assert 'outcome' in result['modules']


class TestBasicResearchTemplate:
    """Basic research template tests"""

    @pytest.fixture
    def template(self):
        return BasicResearchTemplate()

    def test_extract_basic_research(self, template):
        """Test extract basic research"""
        text = """
        Background: Gene regulation mechanism unclear.
        Methods: Cell culture and Western blot.
        Results: Protein expression increased significantly.
        Conclusion: Treatment activates signaling pathway.
        """
        result = template.extract(text)

        assert result['paper_type'] == 'basic_research'
        assert 'scientific_question' in result['modules']
        assert 'research_method' in result['modules']
        assert 'results' in result['modules']
        assert 'conclusion' in result['modules']
        assert 'mechanism' in result['modules']
