"""
API接口测试
"""

import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data


def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_paper_types():
    """测试获取文献类型"""
    response = client.get("/paper-types")
    assert response.status_code == 200
    data = response.json()
    assert "supported_types" in data
    assert "clinical_research" in data["supported_types"]
    assert "case_report" in data["supported_types"]
    assert "basic_research" in data["supported_types"]


def test_analyze_text_clinical():
    """测试分析临床研究文本"""
    text_data = {
        "text": "This randomized controlled trial evaluated a new treatment in 100 patients with diabetes. The intervention group showed significant improvement (p<0.001).",
        "title": "Diabetes Treatment Study"
    }
    response = client.post("/analyze/text", json=text_data)
    assert response.status_code == 200
    data = response.json()
    assert "paper_type" in data
    assert "confidence" in data
    assert "core_info" in data
    assert "full_analysis" in data


def test_analyze_text_case():
    """测试分析病例报告文本"""
    text_data = {
        "text": "Case report: 65-year-old male patient presented with chest pain. Diagnosed with atrial fibrillation. Treated with anticoagulation therapy.",
        "title": "Case Report"
    }
    response = client.post("/analyze/text", json=text_data)
    assert response.status_code == 200
    data = response.json()
    assert data["paper_type"] == "case_report"


def test_analyze_text_basic():
    """测试分析基础研究文本"""
    text_data = {
        "text": "The mechanism of gene regulation was investigated using cell culture experiments. Results showed increased protein expression.",
        "title": "Gene Regulation Study"
    }
    response = client.post("/analyze/text", json=text_data)
    assert response.status_code == 200
    data = response.json()
    assert data["paper_type"] == "basic_research"


def test_analyze_text_too_short():
    """测试文本过短"""
    text_data = {
        "text": "Too short",
        "title": "Test"
    }
    response = client.post("/analyze/text", json=text_data)
    assert response.status_code == 400


def test_analyze_doi():
    """测试分析DOI"""
    # 注意：这个测试需要网络连接，实际情况可能需要mock
    doi_data = {
        "doi": "10.1000/xyz123"
    }
    response = client.post("/analyze/doi", json=doi_data)
    # 由于是测试DOI，可能返回404或500，这是预期的
    assert response.status_code in [400, 404, 500]


def test_analyze_doi_invalid():
    """测试无效DOI"""
    doi_data = {
        "doi": "invalid-doi"
    }
    response = client.post("/analyze/doi", json=doi_data)
    assert response.status_code == 400


def test_analyze_doi_empty():
    """测试空DOI"""
    doi_data = {
        "doi": ""
    }
    response = client.post("/analyze/doi", json=doi_data)
    assert response.status_code == 400
