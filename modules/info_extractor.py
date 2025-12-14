"""
信息提取模块
协调文献分类和结构化提取
"""

from typing import Dict
from .paper_classifier import PaperClassifier
from ..templates.clinical_template import ClinicalResearchTemplate
from ..templates.case_template import CaseReportTemplate
from ..templates.basic_template import BasicResearchTemplate


class InfoExtractor:
    """信息提取器"""

    def __init__(self):
        """初始化提取器"""
        self.classifier = PaperClassifier()
        self.templates = {
            'clinical_research': ClinicalResearchTemplate(),
            'case_report': CaseReportTemplate(),
            'basic_research': BasicResearchTemplate()
        }

    def extract(self, text: str, metadata: Dict = None) -> Dict:
        """
        提取文献信息

        Args:
            text: 文献文本
            metadata: 文献元数据

        Returns:
            包含详细信息的字典

        Raises:
            ValueError: 无法识别的文献类型
        """
        # 分类文献
        classification = self.classifier.get_classification_details(text)
        paper_type = classification['type']
        confidence = classification['confidence']

        # 获取模板
        if paper_type not in self.templates:
            raise ValueError(f"不支持的文献类型: {paper_type}")

        template = self.templates[paper_type]

        # 提取结构化信息
        extracted_info = template.extract(text, metadata)

        # 添加分类信息
        extracted_info['classification'] = {
            'type': paper_type,
            'type_description': classification['type_description'],
            'confidence': confidence
        }

        return extracted_info

    def get_paper_type_description(self, paper_type: str) -> str:
        """
        获取文献类型描述

        Args:
            paper_type: 文献类型

        Returns:
            类型描述
        """
        descriptions = {
            'clinical_research': '临床研究',
            'case_report': '病例报告',
            'basic_research': '基础研究'
        }
        return descriptions.get(paper_type, '未知类型')

    def get_template_modules(self, paper_type: str) -> Dict:
        """
        获取模板模块信息

        Args:
            paper_type: 文献类型

        Returns:
            模块信息字典
        """
        if paper_type not in self.templates:
            return {}

        template = self.templates[paper_type]
        return template.MODULES
