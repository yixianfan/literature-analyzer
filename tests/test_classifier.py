"""
文献类型分类器测试
"""

import pytest
from modules.paper_classifier import PaperClassifier


class TestPaperClassifier:
    """文献分类器测试类"""

    @pytest.fixture
    def classifier(self):
        """创建分类器实例"""
        return PaperClassifier()

    def test_clinical_research_classification(self, classifier):
        """测试临床研究分类"""
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
        """测试病例报告分类"""
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
        """测试基础研究分类"""
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
        """测试获取详细分类信息"""
        text = "This randomized controlled trial included 100 patients..."
        details = classifier.get_classification_details(text)

        assert 'type' in details
        assert 'confidence' in details
        assert 'scores' in details
        assert 'type_description' in details
        assert details['type'] in ['clinical_research', 'case_report', 'basic_research']
