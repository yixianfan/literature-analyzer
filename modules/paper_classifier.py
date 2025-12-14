"""
文献类型识别模块
自动识别文献类型：临床研究、Case报道、基础研究
"""

import re
from typing import Dict, List, Tuple


class PaperClassifier:
    """文献类型分类器"""

    # 临床研究关键词
    CLINICAL_KEYWORDS = {
        'study_design': [
            'randomized controlled trial', 'RCT', 'cohort', 'case-control',
            'cross-sectional', 'prospective', 'retrospective', 'clinical trial',
            '随机对照试验', '队列研究', '病例对照', '横断面研究'
        ],
        'participants': [
            'patients', 'participants', 'subjects', 'n =', 'patients with',
            '患者', '受试者', '研究对象'
        ],
        'intervention': [
            'treatment', 'intervention', 'therapy', 'drug', 'medication',
            'surgery', 'procedure', '治疗', '干预', '药物', '手术'
        ],
        'outcomes': [
            'outcome', 'endpoint', 'efficacy', 'safety', 'effectiveness',
            '结局', '终点', '有效性', '安全性'
        ],
        'statistics': [
            'p-value', 'confidence interval', 'odds ratio', 'hazard ratio',
            '95% CI', 'P <', 'P =', 'p<', '置信区间', '比值比'
        ]
    }

    # Case报道关键词
    CASE_KEYWORDS = {
        'case_report': [
            'case report', 'case presentation', 'case study', '病例报告',
            '病例报道', '案例报告'
        ],
        'patient_info': [
            'patient was', 'patient presented with', 'patient developed',
            '患者', '岁', '年', '男性', '女性'
        ],
        'clinical_features': [
            'presented with', 'complained of', 'diagnosed with',
            '表现为', '主诉', '诊断'
        ],
        'diagnosis': [
            'diagnosis', 'diagnosed', 'confirmed by',
            '诊断', '确诊', '证实'
        ],
        'treatment_outcome': [
            'treatment', 'therapy', 'outcome', 'follow-up',
            '治疗', '疗效', '结果', '随访'
        ]
    }

    # 基础研究关键词
    BASIC_KEYWORDS = {
        'methods': [
            'methodology', 'experiment', 'cell culture', 'mice', 'rats',
            '方法', '实验', '细胞培养', '小鼠', '大鼠'
        ],
        'molecular': [
            'gene', 'protein', 'expression', 'pathway', 'mechanism',
            '基因', '蛋白', '表达', '通路', '机制'
        ],
        'results_data': [
            'increased', 'decreased', 'significant', 'data show',
            '增加', '减少', '显著', '数据显示'
        ],
        'biological': [
            'biological', 'molecular', 'cellular', 'biochemical',
            '生物', '分子', '细胞', '生化'
        ]
    }

    def __init__(self):
        """初始化分类器"""
        self.clinical_patterns = self._compile_patterns(self.CLINICAL_KEYWORDS)
        self.case_patterns = self._compile_patterns(self.CASE_KEYWORDS)
        self.basic_patterns = self._compile_patterns(self.BASIC_KEYWORDS)

    def _compile_patterns(self, keywords_dict: Dict[str, List[str]]) -> Dict[str, List[re.Pattern]]:
        """编译关键词为正则表达式"""
        patterns = {}
        for category, keywords in keywords_dict.items():
            patterns[category] = [
                re.compile(keyword, re.IGNORECASE) for keyword in keywords
            ]
        return patterns

    def classify(self, text: str) -> Tuple[str, float]:
        """
        分类文献类型

        Args:
            text: 文献文本

        Returns:
            Tuple[文献类型, 置信度]
        """
        # 计算各类别得分
        clinical_score = self._calculate_score(text, self.clinical_patterns)
        case_score = self._calculate_score(text, self.case_patterns)
        basic_score = self._calculate_score(text, self.basic_patterns)

        # 计算归一化得分
        scores = {
            'clinical_research': clinical_score,
            'case_report': case_score,
            'basic_research': basic_score
        }

        # 求最高得分
        total_score = sum(scores.values())
        if total_score == 0:
            return 'basic_research', 0.5  # 默认基础研究

        max_type = max(scores, key=scores.get)
        confidence = scores[max_type] / total_score

        return max_type, confidence

    def _calculate_score(self, text: str, patterns: Dict[str, List[re.Pattern]]) -> float:
        """计算文本得分"""
        score = 0.0
        text_lower = text.lower()

        for category, pattern_list in patterns.items():
            matches = sum(1 for pattern in pattern_list if pattern.search(text_lower))
            # 根据类别设置权重
            weight = self._get_category_weight(category)
            score += matches * weight

        return score

    def _get_category_weight(self, category: str) -> float:
        """获取类别权重"""
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
        获取详细分类信息

        Args:
            text: Returns:
             文献文本

       包含详细分类信息的字典
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
                'clinical_research': '临床研究',
                'case_report': '病例报告',
                'basic_research': '基础研究'
            }[paper_type]
        }
