"""
病例报告结构化模板
参考Blood期刊的5大模块
"""

from typing import Dict
import re


class CaseReportTemplate:
    """病例报告的结构化模板（5大模块）"""

    # 模块定义
    MODULES = {
        'case_summary': '病例概述',
        'clinical_presentation': '临床表现',
        'diagnosis': '诊断过程',
        'treatment': '治疗方案',
        'outcome': '治疗结果'
    }

    def extract(self, text: str, metadata: Dict = None) -> Dict:
        """
        从病例报告文本中提取结构化信息

        Args:
            text: 文献全文或摘要文本
            metadata: 文献元数据

        Returns:
            包含5大模块的结构化信息字典
        """
        text_lower = text.lower()

        return {
            'paper_type': 'case_report',
            'modules': {
                'case_summary': self._extract_case_summary(text, text_lower),
                'clinical_presentation': self._extract_clinical_presentation(text, text_lower),
                'diagnosis': self._extract_diagnosis(text, text_lower),
                'treatment': self._extract_treatment(text, text_lower),
                'outcome': self._extract_outcome(text, text_lower)
            },
            'metadata': metadata or {}
        }

    def _extract_case_summary(self, text: str, text_lower: str) -> str:
        """提取病例概述"""
        patterns = [
            r'case report[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. clinical)',
            r'case presentation[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. diagnosis)',
            r'病例概述[:\s]*(.*?)(?=\n\n|临床表现)',
            r'(?:we report|this case) (.*?)(?=\.|,|\n)',
            r'a (?:[0-9]+-year-old|患者) (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        # 如果没有匹配，提取患者信息
        patient_info = self._extract_patient_info(text)
        if patient_info:
            return patient_info

        return "未明确提及病例概述"

    def _extract_clinical_presentation(self, text: str, text_lower: str) -> str:
        """提取临床表现"""
        patterns = [
            r'clinical presentation[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. diagnosis|\. treatment)',
            r'presentation[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. diagnosis)',
            r'临床表现[:\s]*(.*?)(?=\n\n|诊断过程)',
            r'(?:presented with|complained of|chief complaint) (.*?)(?=\.|,|\n)',
            r'(?:主诉|现病史|症状)[:\s]*(.*?)(?=\n\n|诊断)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        return "未明确提及临床表现"

    def _extract_diagnosis(self, text: str, text_lower: str) -> str:
        """提取诊断过程"""
        patterns = [
            r'diagnosis[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. treatment|\. outcome)',
            r'diagnostic[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. treatment)',
            r'诊断过程[:\s]*(.*?)(?=\n\n|治疗方案)',
            r'(?:diagnosed with|diagnosis was|confirmed by) (.*?)(?=\.|,|\n)',
            r'(?:检查结果|实验室检查|影像学)[:\s]*(.*?)(?=\n\n|治疗)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        return "未明确提及诊断过程"

    def _extract_treatment(self, text: str, text_lower: str) -> str:
        """提取治疗方案"""
        patterns = [
            r'treatment[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. outcome|\. follow-up)',
            r'management[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. outcome)',
            r'治疗方案[:\s]*(.*?)(?=\n\n|治疗结果)',
            r'(?:treated with|management included|therapy consisted of) (.*?)(?=\.|,|\n)',
            r'(?:治疗|用药|手术)[:\s]*(.*?)(?=\n\n|结果)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        return "未明确提及治疗方案"

    def _extract_outcome(self, text: str, text_lower: str) -> str:
        """提取治疗结果"""
        patterns = [
            r'outcome[:\s]*(.*?)(?=\n\n|\. [A-Z]|$)',
            r'follow[- ]?up[:\s]*(.*?)(?=\n\n|\. [A-Z]|$)',
            r'治疗结果[:\s]*(.*?)(?=\n\n|$)',
            r'(?:outcome was|patient (?:recovered|improved|deteriorated)) (.*?)(?=\.|,|\n)',
            r'(?:结果|预后|随访)[:\s]*(.*?)(?=\n\n|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        return "未明确提及治疗结果"

    def _extract_patient_info(self, text: str) -> str:
        """提取患者基本信息"""
        patterns = [
            r'([0-9]+-year-old (?:male|female|man|woman).*?)(?=\.|,|\n)',
            r'(患者.*?年.*?岁.*?)(?=\.|,|\n)',
            r'(a [0-9]+ year old .*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text.lower(), re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:300]

        return ""
