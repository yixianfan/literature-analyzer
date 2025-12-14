"""
DOI resolver tests
"""

import pytest
from modules.doi_resolver import DOIResolver


class TestDOIResolver:
    """DOI resolver tests类"""

    @pytest.fixture
    def resolver(self):
        """Create DOI resolver instance"""
        return DOIResolver()

    def test_extract_doi_from_url(self, resolver):
        """Test extract DOI from URL"""
        doi_url = "https://doi.org/10.1000/xyz123"
        doi = resolver._extract_doi(doi_url)
        assert doi == "10.1000/xyz123"

    def test_extract_doi_from_string(self, resolver):
        """Test extract DOI from string"""
        doi_string = "doi: 10.1000/xyz123"
        doi = resolver._extract_doi(doi_string)
        assert doi == "10.1000/xyz123"

    def test_extract_doi_invalid(self, resolver):
        """Test invalid DOI"""
        invalid_string = "not a doi"
        doi = resolver._extract_doi(invalid_string)
        assert doi is None

    def test_doi_pattern(self, resolver):
        """Test DOI pattern"""
        # 有效DOI
        assert resolver.DOI_PATTERN.match("10.1000/xyz123")
        assert resolver.DOI_PATTERN.match("10.1371/journal.pone.0123456")

        # 无效DOI
        assert not resolver.DOI_PATTERN.match("doi: 10.1000/xyz123")
        assert not resolver.DOI_PATTERN.match("invalid doi")

    def test_format_metadata(self, resolver):
        """Test format metadata"""
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
