# Literature Analyzer

A Python-based literature analysis tool that automatically identifies paper types and extracts structured information through API integration.

## Features

- **Automatic Paper Type Classification**: Supports Clinical Research, Case Reports, and Basic Research
- **Structured Information Extraction**: Extracts key information based on journal-standard templates
- **DOI Resolution**: Automatically retrieves paper information via DOI links
- **API Interface**: RESTful API based on FastAPI with comprehensive documentation
- **Robust Error Handling**: Comprehensive validation and exception handling

## Workflow

1. **Input Reception**: Accepts paper text (full/abstract) or DOI links
2. **Type Identification**: Automatically identifies paper type using keyword-based classification
3. **Template Matching**: Selects corresponding structured template based on paper type
4. **Information Extraction**: Uses regex and NLP techniques to extract key information
5. **Result Output**: Returns JSON-formatted structured analysis report

## Project Structure

```
literature_analyzer/
├── main.py                    # FastAPI main application
├── requirements.txt           # Dependency list
├── modules/                   # Core modules
│   ├── paper_classifier.py    # Paper type classifier
│   ├── doi_resolver.py        # DOI resolver
│   └── info_extractor.py      # Information extractor
├── templates/                 # Structured templates
│   ├── clinical_template.py   # Clinical research template (8 modules)
│   ├── case_template.py       # Case report template (5 modules)
│   └── basic_template.py      # Basic research template (5 modules)
├── tests/                     # Test cases
│   ├── test_classifier.py
│   ├── test_doi_resolver.py
│   ├── test_templates.py
│   └── test_api.py
└── docs/                      # Documentation
    └── API.md
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yixianfan/literature-analyzer.git
cd literature-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
python start_server.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Access API documentation
# Open: http://localhost:8000/docs
```

### Test the API

```bash
# Run examples
python examples.py

# Run tests
python run_tests.py
```

## API Usage

### Analyze Text

```bash
curl -X POST "http://localhost:8000/analyze/text" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "This randomized controlled trial evaluated...",
       "title": "Study Title"
     }'
```

### Analyze by DOI

```bash
curl -X POST "http://localhost:8000/analyze/doi" \
     -H "Content-Type: application/json" \
     -d '{"doi": "10.1371/journal.pone.0123456"}'
```

### Python Example

```python
import requests

url = "http://localhost:8000/analyze/text"
data = {
    "text": "This randomized controlled trial evaluated...",
    "title": "Study Title"
}
response = requests.post(url, json=data)
result = response.json()
print(f"Paper Type: {result['paper_type_description']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## Paper Types

### 1. Clinical Research
**Standard**: Lancet journal structure (8 modules)
- Background, Objective, Methods, Participants, Intervention, Outcomes, Results, Conclusion

### 2. Case Report
**Standard**: Blood journal structure (5 modules)
- Case Summary, Clinical Presentation, Diagnosis, Treatment, Outcome

### 3. Basic Research
**Standard Structure** (5 modules)
- Scientific Question, Research Method, Results, Conclusion, Mechanism

## Output Format

```json
{
    "paper_type": "clinical_research",
    "paper_type_description": "Clinical Research",
    "confidence": 0.92,
    "core_info": {
        "background": "Background information...",
        "objective": "Research objective...",
        "methods": "Research methods...",
        "participants": "Study subjects...",
        "intervention": "Intervention details...",
        "outcomes": "Outcome measures...",
        "results": "Study results...",
        "conclusion": "Conclusions..."
    },
    "full_analysis": { ... },
    "generation_time": "2025-12-14 17:02:00"
}
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_classifier.py

# Run with coverage
pytest --cov=modules --cov=templates
```

## Tech Stack

- **Web Framework**: FastAPI 0.104.1
- **HTTP Client**: requests 2.31.0
- **Data Validation**: pydantic 2.5.0
- **Text Processing**: nltk 3.8.1, regex
- **Testing**: pytest 7.4.3
- **Deployment**: uvicorn

## Notes

1. **Network Dependency**: DOI resolution requires internet access
2. **Text Length**: Minimum 10 characters recommended (100+ for best results)
3. **DOI Validity**: Ensure DOI link is accessible
4. **Result Accuracy**: Auto-extracted results are for reference only, manual verification recommended

## Documentation

- **README.md** - Complete project documentation
- **QUICKSTART.md** - Quick start guide
- **docs/API.md** - Detailed API documentation
- **examples.py** - Usage examples

## License

MIT License

## Contributing

Issues and Pull Requests are welcome!
