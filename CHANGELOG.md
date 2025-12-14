# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-15

### Added
- Initial release of Literature Analyzer
- FastAPI-based RESTful API
- Automatic paper type classification (Clinical Research, Case Reports, Basic Research)
- Structured information extraction using journal-specific templates:
  - Lancet format for clinical research (8 modules)
  - Blood format for case reports (5 modules)
  - Standard format for basic research (5 modules)
- DOI resolution and metadata extraction
- CrossRef and PubMed API integration
- Comprehensive test suite with pytest
- Complete documentation (README, DEPLOYMENT guide)
- Usage examples and demos
- Docker support
- GitHub integration

### Features
- Paper type classification with confidence scoring
- JSON response format with metadata
- Input validation and error handling
- Health check endpoint
- Auto-generated API documentation
- Support for both text and DOI input

### Technical Details
- Built with FastAPI 0.104.1
- Uvicorn ASGI server
- Pydantic for data validation
- NLTK for text processing
- Requests for HTTP client

## [Unreleased]

### Planned
- Machine learning-based classification
- Additional journal templates
- PDF text extraction
- Citation network analysis
- Web UI interface
