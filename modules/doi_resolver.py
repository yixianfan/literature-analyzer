"""
DOI Resolution Module
Extracts paper information from DOI links or DOI numbers
"""

import re
import json
import requests
from typing import Dict, Optional
from urllib.parse import quote


class DOIResolver:
    """DOI resolver"""

    # API endpoints
    CROSSREF_API = "https://api.crossref.org/works/"
    PUBMED_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    DOI_PATTERN = re.compile(r'10\.\d+/.*')

    def __init__(self):
        """Initialize the resolver"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Literature-Analyzer/1.0 (mailto:example@example.com)'
        })

    def resolve(self, doi_or_url: str) -> Dict:
        """
        Resolve DOI or DOI URL

        Args:
            doi_or_url: DOI string or DOI URL

        Returns:
            Dictionary containing paper metadata

        Raises:
            ValueError: Invalid DOI
            requests.RequestException: Network request failed
        """
        # Extract DOI
        doi = self._extract_doi(doi_or_url)
        if not doi:
            raise ValueError(f"Unable to extract valid DOI: {doi_or_url}")

        # Try to get data from CrossRef API first
        try:
            metadata = self._get_from_crossref(doi)
            if metadata:
                return self._format_metadata(metadata, doi)
        except Exception as e:
            print(f"CrossRef API request failed: {e}")

        # If CrossRef fails, try PubMed
        try:
            metadata = self._get_from_pubmed(doi)
            if metadata:
                return self._format_metadata(metadata, doi)
        except Exception as e:
            print(f"PubMed API request failed: {e}")

        raise ValueError(f"Unable to retrieve paper information for DOI {doi}")

    def _extract_doi(self, input_str: str) -> Optional[str]:
        """
        Extract DOI from string

        Args:
            input_str: DOI string or DOI URL

        Returns:
            DOI string or None
        """
        # Clean string
        input_str = input_str.strip()

        # Extract DOI from doi.org or dx.doi.org URL
        if 'doi.org' in input_str or 'dx.doi.org' in input_str:
            # Extract DOI part
            match = self.DOI_PATTERN.search(input_str)
            return match.group(0) if match else None

        # Direct DOI match
        if self.DOI_PATTERN.match(input_str):
            return input_str

        # Search for DOI in string
        match = self.DOI_PATTERN.search(input_str)
        return match.group(0) if match else None

    def _get_from_crossref(self, doi: str) -> Optional[Dict]:
        """Get metadata from CrossRef API"""
        url = f"{self.CROSSREF_API}{quote(doi)}"
        response = self.session.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get('message')

        return None

    def _get_from_pubmed(self, doi: str) -> Optional[Dict]:
        """Get metadata from PubMed API"""
        # Search for PubMed ID by DOI first
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

        # Get detailed information
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
        Format metadata

        Args:
            metadata: Raw metadata
            doi: DOI string

        Returns:
            Formatted metadata dictionary
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

        # Extract title
        if isinstance(metadata.get('title'), list) and metadata['title']:
            formatted['title'] = metadata['title'][0]
        elif isinstance(metadata.get('title'), str):
            formatted['title'] = metadata['title']

        # Extract authors
        authors = metadata.get('author', [])
        if authors:
            formatted['authors'] = [
                f"{author.get('given', '')} {author.get('family', '')}".strip()
                for author in authors
            ]

        # Extract journal name
        if isinstance(metadata.get('container-title'), list) and metadata['container-title']:
            formatted['journal'] = metadata['container-title'][0]

        # Extract publication date
        if 'published-print' in metadata:
            date_parts = metadata['published-print'].get('date-parts', [[]])[0]
            formatted['publication_date'] = '-'.join(map(str, date_parts))
        elif 'published-online' in metadata:
            date_parts = metadata['published-online'].get('date-parts', [[]])[0]
            formatted['publication_date'] = '-'.join(map(str, date_parts))

        # Extract abstract
        if 'abstract' in metadata:
            abstract = metadata['abstract']
            # Remove XML tags
            abstract = re.sub(r'<[^>]+>', '', abstract)
            formatted['abstract'] = abstract.strip()

        # Extract keywords
        if 'subject' in metadata:
            formatted['keywords'] = metadata['subject']

        # Extract volume, issue, pages
        if 'volume' in metadata:
            formatted['volume'] = metadata['volume']
        if 'issue' in metadata:
            formatted['issue'] = metadata['issue']
        if 'page' in metadata:
            formatted['pages'] = metadata['page']

        return formatted

    def extract_full_text(self, doi: str) -> Optional[str]:
        """
        Try to extract full text (usually only abstract available)

        Args:
            doi: DOI string

        Returns:
            Full text or None
        """
        try:
            metadata = self.resolve(doi)
            abstract = metadata.get('abstract', '')
            title = metadata.get('title', '')

            # Combine title and abstract as full text
            full_text = f"{title}\n\n{abstract}"
            return full_text if full_text.strip() else None

        except Exception:
            return None
