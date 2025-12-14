"""
基础研究结构化模板
按照"科学问题-研究方法-研究结果-研究结论-作用机制"模块
"""

from typing import Dict
import re


class BasicResearchTemplate:
    """基础研究的结构化模板（5大模块）"""

    # 模块定义
    MODULES = {
        'scientific_question': '科学问题',
        'research_method': '研究方法',
        'results': '研究结果',
        'conclusion': '研究结论',
        'mechanism': '作用机制'
    }

    def extract(self, text: str, metadata: Dict = None) -> Dict:
        """
        从基础研究文本中提取结构化信息

        Args:
            text: 文献全文或摘要文本
            metadata: 文献元数据

        Returns:
            包含5大模块的结构化信息字典
        """
        text_lower = text.lower()

        return {
            'paper_type': 'basic_research',
            'modules': {
                'scientific_question': self._extract_scientific_question(text, text_lower),
                'research_method': self._extract_research_method(text, text_lower),
                'results': self._extract_results(text, text_lower),
                'conclusion': self._extract_conclusion(text, text_lower),
                'mechanism': self._extract_mechanism(text, text_lower)
            },
            'metadata': metadata or {}
        }

    def _extract_scientific_question(self, text: str, text_lower: str) -> str:
        """提取科学问题"""
        patterns = [
            r'(?:background|introduction)[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. methods|\. objective)',
            r'(?:scientific question|research question)[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'科学问题[:\s]*(.*?)(?=\n\n|研究方法)',
            r'(?:we sought to|we aimed to|the purpose was) (.*?)(?=\.|,|\n)',
            r'(?:however|然而|但是) (.*?)(?=\.|,|\n)',
            r'研究.*?(?:目的|意义|价值) (.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:400]

        # 查找研究空白
        gap_patterns = [
            r'(?:however|然而) (.*?)(?:remains|仍需|仍待) (.*?)(?=\.|,|\n)',
            r'(?:gaps|空白) (?:in|存在) (.*?)(?=\.|,|\n)'
        ]

        for pattern in gap_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(0).strip()[:400]

        return "未明确提及科学问题"

    def _extract_research_method(self, text: str, text_lower: str) -> str:
        """提取研究方法"""
        patterns = [
            r'methods[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. results|\. conclusion)',
            r'methodology[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. results)',
            r'研究方法[:\s]*(.*?)(?=\n\n|研究结果)',
            r'(?:we (?:used|performed|conducted|measured)) (.*?)(?=\.|,|\n)',
            r'(?:cell culture|western blot|qPCR|mice|rat) (.*?)(?=\.|,|\n)',
            r'(?:实验方法|实验设计)[:\s]*(.*?)(?=\n\n|结果)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        return "未明确提及研究方法"

    def _extract_results(self, text: str, text_lower: str) -> str:
        """提取研究结果"""
        patterns = [
            r'results[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. conclusion|\. discussion)',
            r'研究结果[:\s]*(.*?)(?=\n\n|研究结论)',
            r'(?:we found|results show|showed|found that) (.*?)(?=\.|,|\n)',
            r'(?:significant|increased|decreased|enhanced|reduced) (.*?)(?=\.|,|\n)',
            r'(?:expression|levels|activity) (?:of|were) (.*?)(?=\.|,|\n)',
            r'(p\s*[<=>]\s*0\.\d+.*?)(?=\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                result = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
                return result.strip()[:600]

        return "未明确提及研究结果"

    def _extract_conclusion(self, text: str, text_lower: str) -> str:
        """提取研究结论"""
        patterns = [
            r'conclusion[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. discussion|$)',
            r'discussion[:\s]*(.*?)(?=\n\n|\. [A-Z]|$)',
            r'研究结论[:\s]*(.*?)(?=\n\n|$)',
            r'(?:in conclusion|these findings|demonstrate that|indicates that) (.*?)(?=\.|,|\n|$)',
            r'(?:consequently|therefore|thus) (.*?)(?=\.|,|\n|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        return "未明确提及研究结论"

    def _extract_mechanism(self, text: str, text_lower: str) -> str:
        """提取作用机制"""
        patterns = [
            r'mechanism[:\s]*(.*?)(?=\n\n|\. [A-Z]|\. conclusion|$)',
            r'(?:mechanism of action|pathway|signaling)[:\s]*(.*?)(?=\n\n|\. [A-Z])',
            r'作用机制[:\s]*(.*?)(?=\n\n|研究结论)',
            r'(?:through|via|by) (.*?)(?:pathway|mechanism|process) (.*?)(?=\.|,|\n)',
            r'(?:regulates|activates|inhibits|mediates) (.*?)(?=\.|,|\n)',
            r'(?:分子机制|信号通路|调控机制)[:\s]*(.*?)(?=\n\n|结论)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]

        # 查找分子相互作用
        interaction_patterns = [
            r'(?:interaction|相互作用|结合) (?:between|between) (.*?)(?=\.|,|\n)',
            r'(?:up[- ]?regulation|down[- ]?regulation|上调|下调) (.*?)(?=\.|,|\n)'
        ]

        for pattern in interaction_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(0).strip()[:500]

        return "未明确提及作用机制"
