"""
文献整理在线工具
支持API接入，自动识别文献类型并提取结构化信息
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


# 数据模型
class TextInput(BaseModel):
    """文本输入模型"""
    text: str = Field(..., min_length=10, description="文献全文或摘要文本")
    title: Optional[str] = Field(None, description="文献标题")


class DOIInput(BaseModel):
    """DOI输入模型"""
    doi: str = Field(..., description="DOI字符串或DOI链接")


class AnalysisResponse(BaseModel):
    """分析响应模型"""
    paper_type: str
    paper_type_description: str
    confidence: float
    core_info: Dict
    full_analysis: Dict
    generation_time: str


# 创建FastAPI应用
app = FastAPI(
    title="文献整理在线工具",
    description="自动识别文献类型并提取结构化信息的API工具",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 初始化组件
doi_resolver = DOIResolver()
info_extractor = InfoExtractor()


@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "name": "文献整理在线工具",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze_text": "/analyze/text - 分析文献文本",
            "analyze_doi": "/analyze/doi - 通过DOI分析文献",
            "health": "/health - 健康检查",
            "paper_types": "/paper-types - 获取支持的文献类型"
        }
    }


@app.post("/analyze/text", response_model=AnalysisResponse)
async def analyze_text(input_data: TextInput):
    """
    分析文献文本

    Args:
        input_data: 文献文本数据

    Returns:
        结构化分析结果
    """
    try:
        # 验证文本
        if not input_data.text or len(input_data.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="文本内容过短，至少需要10个字符")

        # 执行提取
        extracted_info = info_extractor.extract(input_data.text)

        # 构建响应
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
        raise HTTPException(status_code=500, detail=f"分析文本时发生错误: {str(e)}")


@app.post("/analyze/doi", response_model=AnalysisResponse)
async def analyze_doi(input_data: DOIInput):
    """
    通过DOI分析文献

    Args:
        input_data: DOI数据

    Returns:
        结构化分析结果
    """
    try:
        # 验证DOI
        if not input_data.doi:
            raise HTTPException(status_code=400, detail="DOI不能为空")

        # 通过DOI获取元数据
        metadata = doi_resolver.resolve(input_data.doi)

        # 提取全文文本
        text_content = doi_resolver.extract_full_text(input_data.doi)

        if not text_content:
            # 如果无法获取全文，使用标题作为文本
            text_content = metadata.get('title', '')

        if not text_content or len(text_content.strip()) < 10:
            raise HTTPException(
                status_code=404,
                detail="无法获取足够的文献内容进行分析"
            )

        # 执行提取
        extracted_info = info_extractor.extract(text_content, metadata)

        # 构建响应
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
        raise HTTPException(status_code=500, detail=f"分析DOI时发生错误: {str(e)}")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/paper-types")
async def get_paper_types():
    """获取支持的文献类型"""
    return {
        "supported_types": {
            "clinical_research": {
                "name": "临床研究",
                "description": "临床试验、队列研究等临床研究",
                "modules": info_extractor.get_template_modules('clinical_research')
            },
            "case_report": {
                "name": "病例报告",
                "description": "病例报告、案例分析",
                "modules": info_extractor.get_template_modules('case_report')
            },
            "basic_research": {
                "name": "基础研究",
                "description": "基础实验、机制研究",
                "modules": info_extractor.get_template_modules('basic_research')
            }
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "服务器内部错误",
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
