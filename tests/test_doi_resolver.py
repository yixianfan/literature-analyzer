"""
DOI解析器测试
"""

import pytest
from modules.doi_resolver import DOIResolver


class TestDOIResolver:
    """DOI解析器测试类"""

    @pytest.fixture
    def resolver(self):
        """创建DOI解析器实例"""
        return DOIResolver()

    def test_extract_doi_from_url(self, resolver):
        """测试从URL中提取DOI"""
        doi_url = "https://doi.org/10.1000/xyz123"
        doi = resolver._extract_doi(doi_url)
        assert doi == "10.1000/xyz123"

    def test_extract_doi_from_string(self, resolver):
        """测试从字符串中提取DOI"""
        doi_string = "doi: 10.1000/xyz123"
        doi = resolver._extract_doi(doi_string)
        assert doi == "10.1000/xyz123"

    def test_extract_doi_invalid(self, resolver):
        """测试无效DOI"""
        invalid_string = "not a doi"
        doi = resolver._extract_doi(invalid_string)
        assert doi is None

    def test_doi_pattern(self, resolver):
        """测试DOI模式匹配"""
        # 有效DOI
        assert resolver.DOI_PATTERN.match("10.1000/xyz123")
        assert resolver.DOI_PATTERN.match("10.1371/journal.pone.0123456")

        # 无效DOI
        assert not resolver.DOI_PATTERN.match("doi: 10.1000/xyz123")
        assert not resolver.DOI_PATTERN.match("invalid doi")

    def test_format_metadata(self, resolver):
        """测试元数据格式化"""
        # 模拟CrossRef API响应
        mock_metadata = {
            'title': ['Test Article'],
            'author': [{'given': 'John', 'family': 'Doe'}],
            'container-title': ['Test Journal'],
            'published-print': {'date-parts': [[2023, 1, 1]]},
            'abstract': '<p>Test abstract</p>',
            'volume': '1',
            'issue': '1',
            'page': '1-10'
        }

        formatted = resolver._format_metadata(mock_metadata, "10.1000/test")

        assert formatted['doi'] == "10.1000/test"
        assert formatted['title'] == "Test Article"
        assert len(formatted['authors']) == 1
        assert formatted['journal'] == "Test Journal"
        assert formatted['abstract'] == "Test abstract"
