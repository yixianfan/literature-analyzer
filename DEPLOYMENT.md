# Literature Analyzer - Deployment Guide

## Overview
A FastAPI-based tool for automatic paper type classification and structured information extraction from academic literature.

## Features
- **Paper Type Classification**: Automatically identifies Clinical Research, Case Reports, and Basic Research
- **Structured Extraction**: Extracts key information using journal-specific templates
- **DOI Support**: Retrieve and analyze papers via DOI
- **RESTful API**: Easy integration with web applications
- **Comprehensive Documentation**: Auto-generated API docs

## System Requirements
- Python 3.8+
- 2GB RAM (minimum)
- Internet connection (for DOI resolution)

## Installation

### Option 1: Quick Install
```bash
# Clone the repository
git clone <repository-url>
cd literature_analyzer

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

### Option 2: Using Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

## Running the Application

### Development Mode
```bash
cd literature_analyzer
python main.py
```

Server will start at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Production Mode
```bash
# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### 1. Analyze Text
**Endpoint**: `POST /analyze/text`

**Request Body**:
```json
{
  "text": "Full paper text or abstract...",
  "title": "Paper Title (optional)"
}
```

**Response**:
```json
{
  "paper_type": "clinical_research",
  "paper_type_description": "Clinical Research",
  "confidence": 0.85,
  "core_info": {
    "background": "...",
    "objective": "...",
    "methods": "...",
    "participants": "...",
    "intervention": "...",
    "outcomes": "...",
    "results": "...",
    "conclusion": "..."
  },
  "generation_time": "2025-12-15 00:00:00"
}
```

## Testing

### Run Unit Tests
```bash
cd literature_analyzer
python -m pytest tests/ -v
```
