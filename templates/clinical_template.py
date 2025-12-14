"""
临床研究结构化模板
参考Lancet期刊的8大模块
"""

from typing import Dict, List
import re


class ClinicalResearchTemplate:
    """临床研究的结构化模板（8大模块）"""

    # 模块定义
    MODULES = {
        'background': '研究背景',
        'objective': '研究目的',
        'methods': '研究方法',
        'participants': '研究对象',
        'intervention': '干预措施',
        'outcomes': '结局指标',
        'results': '研究结果',
        'conclusion': '结论'
    }

    def extract(self, text: str, metadata: Dict = None) -> Dict:
        """
        从临床研究文本中提取结构化信息

        Args:
            text: 文献全文或摘要文本
            metadata: 文献元数据

        Returns:
            包含8大模块的结构化信息字典
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
        """提取研究背景"""
        patterns = [
            r'background[:\s]*(.*?)(?=\n\n|\. [A-Z]|\.objective|\. methods)',
            r'introduction[:\s]*(.*?)(?=\n\n|\. [A-Z]|\.objective)',
            r'研究背景[:\s]*(.*?)(?=\n\n|研究目的)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]  # 限制长度

        # 兜底：取前200字符
        return text[:200].strip() + "..."

    def _extract_objective(self, text: str, text_lower: str) -> str:
        """提取研究目的"""
        patterns = [
            r'objective[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. methods|\.participants)',
            r'aim[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'研究目的[:\s]*(.*?)(?=\n\n|研究方法)',
            r'to (?:investigate|evaluate|assess|determine) (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:300]

        return "未明确提及研究目的"

    def _extract_methods(self, text: str, text_lower: str) -> str:
        """提取研究方法"""
        patterns = [
            r'methods[:\s]*(.*?)(?=\n\n|\. [A-Z]|\.participants|\. intervention)',
            r'methodology[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'研究方法[:\s]*(.*?)(?=\n\n|研究对象)',
            r'(?:we conducted|this was) (.*?)(?:study|trial)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        return "未明确提及研究方法"

    def _extract_participants(self, text: str, text_lower: str) -> str:
        """提取研究对象"""
        patterns = [
            r'participants[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. intervention|\. outcomes)',
            r'study population[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'研究对象[:\s]*(.*?)(?=\n\n|干预措施)',
            r'(?:patients|participants) (?:with|aged|n =) (.*?)(?=\.|,|\n)',
            r'(\d+) patients? (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(0).strip()[:400]

        return "未明确提及研究对象信息"

    def _extract_intervention(self, text: str, text_lower: str) -> str:
        """提取干预措施"""
        patterns = [
            r'intervention[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. outcomes|\. results)',
            r'treatment[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. outcomes)',
            r'干预措施[:\s]*(.*?)(?=\n\n|结局指标)',
            r'(?:treatment|intervention) (?:with|using|consisted of) (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:400]

        return "未明确提及干预措施"

    def _extract_outcomes(self, text: str, text_lower: str) -> str:
        """提取结局指标"""
        patterns = [
            r'outcomes[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. results|\. conclusion)',
            r'primary outcome[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'结局指标[:\s]*(.*?)(?=\n\n|研究结果)',
            r'(?:primary|main) (?:outcome|endpoint) (?:was|were) (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:400]

        return "未明确提及结局指标"

    def _extract_results(self, text: str, text_lower: str) -> str:
        """提取研究结果"""
        patterns = [
            r'results[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. conclusion|\. interpretation)',
            r'研究结果[:\s]*(.*?)(?=\n\n|结论)',
            r'(?:we found|results show|showed) (.*?)(?=\.|,|\n)',
            r'(p\s*[<=>]\s*0\.\d+.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                result = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
                return result.strip()[:600]

        return "未明确提及研究结果"

    def _extract_conclusion(self, text: str, text_lower: str) -> str:
        """提取结论"""
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

        return "未明确提及结论"
