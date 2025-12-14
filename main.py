"""
Literature Analyzer Tool
A FastAPI-based tool for automatic paper type classification and structured information extraction
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict
import uvicorn
from datetime import datetime
import traceback

from modules.doi_resolver import DOIResolver
from modules.info_extractor import InfoExtractor


# Data models
class TextInput(BaseModel):
    """Text input model"""
    text: str = Field(..., min_length=10, description="Full text or abstract of the paper")
    title: Optional[str] = Field(None, description="Title of the paper")


class DOIInput(BaseModel):
    """DOI input model"""
    doi: str = Field(..., description="DOI string or DOI URL")


class AnalysisResponse(BaseModel):
    """Analysis response model"""
    paper_type: str
    paper_type_description: str
    confidence: float
    core_info: Dict
    full_analysis: Dict
    generation_time: str


# Create FastAPI application
app = FastAPI(
    title="Literature Analyzer",
    description="API tool for automatic paper type classification and structured information extraction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize components
doi_resolver = DOIResolver()
info_extractor = InfoExtractor()


@app.get("/")
async def root():
    """Root endpoint, returns API information"""
    return {
        "name": "Literature Analyzer",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze_text": "/analyze/text - Analyze paper text",
            "analyze_doi": "/analyze/doi - Analyze paper by DOI",
            "health": "/health - Health check",
            "paper_types": "/paper-types - Get supported paper types"
        }
    }


@app.post("/analyze/text", response_model=AnalysisResponse)
async def analyze_text(input_data: TextInput):
    """
    Analyze paper text

    Args:
        input_data: Paper text data

    Returns:
        Structured analysis results
    """
    try:
        # Validate text
        if not input_data.text or len(input_data.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text content too short, minimum 10 characters required")

        # Perform extraction
        extracted_info = info_extractor.extract(input_data.text)

        # Build response
        response = AnalysisResponse(
            paper_type=extracted_info['classification']['type'],
            paper_type_description=extracted_info['classification']['type_description'],
            confidence=extracted_info['classification']['confidence'],
            core_info=extracted_info['modules'],
            full_analysis=extracted_info,
            generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")


@app.post("/analyze/doi", response_model=AnalysisResponse)
async def analyze_doi(input_data: DOIInput):
    """
    Analyze paper by DOI

    Args:
        input_data: DOI data

    Returns:
        Structured analysis results
    """
    try:
        # Validate DOI
        if not input_data.doi:
            raise HTTPException(status_code=400, detail="DOI cannot be empty")

        # Get metadata from DOI
        metadata = doi_resolver.resolve(input_data.doi)

        # Extract full text
        text_content = doi_resolver.extract_full_text(input_data.doi)

        if not text_content:
            # If full text not available, use title as text
            text_content = metadata.get('title', '')

        if not text_content or len(text_content.strip()) < 10:
            raise HTTPException(
                status_code=404,
                detail="Unable to retrieve sufficient paper content for analysis"
            )

        # Perform extraction
        extracted_info = info_extractor.extract(text_content, metadata)

        # Build response
        response = AnalysisResponse(
            paper_type=extracted_info['classification']['type'],
            paper_type_description=extracted_info['classification']['type_description'],
            confidence=extracted_info['classification']['confidence'],
            core_info=extracted_info['modules'],
            full_analysis=extracted_info,
            generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing DOI: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/paper-types")
async def get_paper_types():
    """Get supported paper types"""
    return {
        "supported_types": {
            "clinical_research": {
                "name": "Clinical Research",
                "description": "Clinical trials, cohort studies, and other clinical research",
                "modules": info_extractor.get_template_modules('clinical_research')
            },
            "case_report": {
                "name": "Case Report",
                "description": "Case reports and case studies",
                "modules": info_extractor.get_template_modules('case_report')
            },
            "basic_research": {
                "name": "Basic Research",
                "description": "Basic experiments and mechanism studies",
                "modules": info_extractor.get_template_modules('basic_research')
            }
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "traceback": traceback.format_exc() if app.debug else None
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
