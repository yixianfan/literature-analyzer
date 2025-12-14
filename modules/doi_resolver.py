"""
DOI解析模块
从DOI链接或DOI号提取文献信息
"""

import re
import json
import requests
from typing import Dict, Optional
from urllib.parse import quote


class DOIResolver:
    """DOI解析器"""

    # API endpoints
    CROSSREF_API = "https://api.crossref.org/works/"
    PUBMED_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    DOI_PATTERN = re.compile(r'10\.\d+/.*')

    def __init__(self):
        """初始化解析器"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Literature-Analyzer/1.0 (mailto:example@example.com)'
        })

    def resolve(self, doi_or_url: str) -> Dict:
        """
        解析DOI或DOI URL

        Args:
            doi_or_url: DOI字符串或DOI URL

        Returns:
            文献元数据字典

        Raises:
            ValueError: 无效的DOI
            requests.RequestException: 网络请求失败
        """
        # 提取DOI
        doi = self._extract_doi(doi_or_url)
        if not doi:
            raise ValueError(f"无法提取有效DOI: {doi_or_url}")

        # 首先尝试从CrossRef API获取数据
        try:
            metadata = self._get_from_crossref(doi)
            if metadata:
                return self._format_metadata(metadata, doi)
        except Exception as e:
            print(f"CrossRef API请求失败: {e}")

        # 如果CrossRef失败则尝试PubMed
        try:
            metadata = self._get_from_pubmed(doi)
            if metadata:
                return self._format_metadata(metadata, doi)
        except Exception as e:
            print(f"PubMed API请求失败: {e}")

        raise ValueError(f"无法获取DOI {doi} 的文献信息")

    def _extract_doi(self, input_str: str) -> Optional[str]:
        """
        从字符串中提取DOI

        Args:
            input_str: DOI字符串或DOI URL

        Returns:
            DOI字符串或None
        """
        # 清理字符串
        input_str = input_str.strip()

        # 提取doi.org或dx.doi.org URL中的DOI
        if 'doi.org' in input_str or 'dx.doi.org' in input_str:
            # 提取DOI部分
            match = self.DOI_PATTERN.search(input_str)
            return match.group(0) if match else None

        # 直接匹配DOI
        if self.DOI_PATTERN.match(input_str):
            return input_str

        # 在字符串中搜索DOI
        match = self.DOI_PATTERN.search(input_str)
        return match.group(0) if match else None

    def _get_from_crossref(self, doi: str) -> Optional[Dict]:
        """从CrossRef API获取元数据"""
        url = f"{self.CROSSREF_API}{quote(doi)}"
        response = self.session.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get('message')

        return None

    def _get_from_pubmed(self, doi: str) -> Optional[Dict]:
        """从PubMed API获取元数据"""
        # 首先通过DOI搜索PubMed ID
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            'db': 'pubmed',
            'term': doi,
            'retmode': 'json'
        }

        search_response = self.session.get(search_url, params=search_params, timeout=10)
        if search_response.status_code != 200:
            return None

        search_data = search_response.json()
        id_list = search_data.get('esearchresult', {}).get('idlist', [])

        if not id_list:
            return None

        # 获取详细信息
        pubmed_id = id_list[0]
        summary_params = {
            'db': 'pubmed',
            'id': pubmed_id,
            'retmode': 'json'
        }

        summary_response = self.session.get(self.PUBMED_API, params=summary_params, timeout=10)
        if summary_response.status_code == 200:
            summary_data = summary_response.json()
            return summary_data.get('result', {}).get(pubmed_id)

        return None

    def _format_metadata(self, metadata: Dict, doi: str) -> Dict:
        """
        格式化元数据

        Args:
            metadata: 原始元数据
            doi: DOI字符串

        Returns:
            格式化后的元数据字典
        """
        formatted = {
            'doi': doi,
            'title': '',
            'authors': [],
            'journal': '',
            'publication_date': '',
            'abstract': '',
            'keywords': [],
            'volume': '',
            'issue': '',
            'pages': '',
            'url': f'https://doi.org/{doi}'
        }

        # 提取标题
        if isinstance(metadata.get('title'), list) and metadata['title']:
            formatted['title'] = metadata['title'][0]
        elif isinstance(metadata.get('title'), str):
            formatted['title'] = metadata['title']

        # 提取作者
        authors = metadata.get('author', [])
        if authors:
            formatted['authors'] = [
                f"{author.get('given', '')} {author.get('family', '')}".strip()
                for author in authors
            ]

        # 提取期刊名称
        if isinstance(metadata.get('container-title'), list) and metadata['container-title']:
            formatted['journal'] = metadata['container-title'][0]

        # 提取发表日期
        if 'published-print' in metadata:
            date_parts = metadata['published-print'].get('date-parts', [[]])[0]
            formatted['publication_date'] = '-'.join(map(str, date_parts))
        elif 'published-online' in metadata:
            date_parts = metadata['published-online'].get('date-parts', [[]])[0]
            formatted['publication_date'] = '-'.join(map(str, date_parts))

        # 提取摘要
        if 'abstract' in metadata:
            abstract = metadata['abstract']
            # 移除XML标签
            abstract = re.sub(r'<[^>]+>', '', abstract)
            formatted['abstract'] = abstract.strip()

        # 提取关键词
        if 'subject' in metadata:
            formatted['keywords'] = metadata['subject']

        # 提取卷期页码
        if 'volume' in metadata:
            formatted['volume'] = metadata['volume']
        if 'issue' in metadata:
            formatted['issue'] = metadata['issue']
        if 'page' in metadata:
            formatted['pages'] = metadata['page']

        return formatted

    def extract_full_text(self, doi: str) -> Optional[str]:
        """
        尝试提取全文（通常只有摘要）

        Args:
            doi: DOI字符串

        Returns:
            全文文本或None
        """
        try:
            metadata = self.resolve(doi)
            abstract = metadata.get('abstract', '')
            title = metadata.get('title', '')

            # 拼接标题和摘要作为全文
            full_text = f"{title}\n\n{abstract}"
            return full_text if full_text.strip() else None

        except Exception:
            return None
