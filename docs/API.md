# API 详细文档

## 概述

文献整理在线工具提供基于FastAPI的RESTful API，支持文献文本分析和DOI解析。

## 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`
- **响应格式**: JSON

## 接口列表

### 1. 获取API信息

**接口地址**: `GET /`

**描述**: 获取API基本信息和支持的端点

**响应示例**:
```json
{
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
```

### 2. 健康检查

**接口地址**: `GET /health`

**描述**: 检查服务是否正常运行

**响应示例**:
```json
{
    "status": "healthy",
    "timestamp": "2025-12-14 17:02:00"
}
```

### 3. 获取支持的文献类型

**接口地址**: `GET /paper-types`

**描述**: 获取系统支持的文献类型及其模块定义

**响应示例**:
```json
{
    "supported_types": {
        "clinical_research": {
            "name": "临床研究",
            "description": "临床试验、队列研究等临床研究",
            "modules": {
                "background": "研究背景",
                "objective": "研究目的",
                "methods": "研究方法",
                "participants": "研究对象",
                "intervention": "干预措施",
                "outcomes": "结局指标",
                "results": "研究结果",
                "conclusion": "结论"
            }
        },
        "case_report": {
            "name": "病例报告",
            "description": "病例报告、案例分析",
            "modules": {
                "case_summary": "病例概述",
                "clinical_presentation": "临床表现",
                "diagnosis": "诊断过程",
                "treatment": "治疗方案",
                "outcome": "治疗结果"
            }
        },
        "basic_research": {
            "name": "基础研究",
            "description": "基础实验、机制研究",
            "modules": {
                "scientific_question": "科学问题",
                "research_method": "研究方法",
                "results": "研究结果",
                "conclusion": "研究结论",
                "mechanism": "作用机制"
            }
        }
    }
}
```

### 4. 分析文献文本

**接口地址**: `POST /analyze/text`

**描述**: 分析输入的文献文本，自动识别类型并提取结构化信息

**请求参数**:
```json
{
    "text": "string - 文献全文或摘要文本（必需，最少10字符）",
    "title": "string - 文献标题（可选）"
}
```

**请求示例**:
```bash
curl -X POST "http://localhost:8000/analyze/text" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "This randomized controlled trial evaluated the efficacy of a new antihypertensive drug in patients with stage 2 hypertension. Methods: We conducted a double-blind, placebo-controlled trial involving 200 patients. Results: The treatment group showed significant reduction in systolic blood pressure (p<0.001). Conclusion: The new drug is effective for hypertension treatment.",
       "title": "Efficacy of New Antihypertensive Drug"
     }'
```

**响应示例**:
```json
{
    "paper_type": "clinical_research",
    "paper_type_description": "临床研究",
    "confidence": 0.92,
    "core_info": {
        "background": "高血压治疗的临床研究...",
        "objective": "评估新的降压药物疗效...",
        "methods": "双盲、安慰剂对照试验...",
        "participants": "200名患者...",
        "intervention": "新的降压药物...",
        "outcomes": "收缩压降低...",
        "results": "治疗组收缩压显著降低 (p<0.001)...",
        "conclusion": "新药对高血压治疗有效..."
    },
    "full_analysis": {
        "paper_type": "clinical_research",
        "modules": { ... },
        "classification": {
            "type": "clinical_research",
            "type_description": "临床研究",
            "confidence": 0.92
        },
        "metadata": {}
    },
    "generation_time": "2025-12-14 17:02:00"
}
```

**错误响应**:
- `400 Bad Request`: 文本过短或格式错误
- `500 Internal Server Error`: 服务器内部错误

### 5. 通过DOI分析文献

**接口地址**: `POST /analyze/doi`

**描述**: 通过DOI链接或DOI号获取文献信息并进行分析

**请求参数**:
```json
{
    "doi": "string - DOI字符串或DOI链接（必需）"
}
```

**请求示例**:
```bash
curl -X POST "http://localhost:8000/analyze/doi" \
     -H "Content-Type: application/json" \
     -d '{"doi": "10.1371/journal.pone.0123456"}'
```

**响应示例**:
```json
{
    "paper_type": "basic_research",
    "paper_type_description": "基础研究",
    "confidence": 0.88,
    "core_info": {
        "scientific_question": "基因调控机制研究...",
        "research_method": "细胞培养和Western blot...",
        "results": "蛋白表达显著增加...",
        "conclusion": "治疗激活信号通路...",
        "mechanism": "通过蛋白质上调激活..."
    },
    "full_analysis": {
        "paper_type": "basic_research",
        "modules": { ... },
        "classification": {
            "type": "basic_research",
            "type_description": "基础研究",
            "confidence": 0.88
        },
        "metadata": {
            "doi": "10.1371/journal.pone.0123456",
            "title": "Gene Regulation Mechanism Study",
            "authors": ["John Doe", "Jane Smith"],
            "journal": "PLOS ONE",
            "publication_date": "2023-01-01",
            "abstract": "We investigated the molecular mechanism...",
            "url": "https://doi.org/10.1371/journal.pone.0123456"
        }
    },
    "generation_time": "2025-12-14 17:02:00"
}
```

**错误响应**:
- `400 Bad Request`: 无效的DOI
- `404 Not Found`: 无法获取文献内容
- `500 Internal Server Error`: 服务器内部错误

## 代码示例

### Python 示例

```python
import requests
import json

# 配置
BASE_URL = "http://localhost:8000"

# 分析文本
def analyze_text(text, title=None):
    url = f"{BASE_URL}/analyze/text"
    data = {"text": text}
    if title:
        data["title"] = title

    response = requests.post(url, json=data)
    return response.json()

# 通过DOI分析
def analyze_doi(doi):
    url = f"{BASE_URL}/analyze/doi"
    data = {"doi": doi}

    response = requests.post(url, json=data)
    return response.json()

# 获取文献类型
def get_paper_types():
    url = f"{BASE_URL}/paper-types"
    response = requests.get(url)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 分析临床研究文本
    clinical_text = """
    Background: This randomized controlled trial evaluated a new treatment.
    Methods: We included 100 patients in the study.
    Results: Significant improvement was observed (p<0.001).
    Conclusion: The treatment is effective.
    """
    result = analyze_text(clinical_text, "Clinical Trial Study")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 分析DOI
    doi_result = analyze_doi("10.1371/journal.pone.0123456")
    print(json.dumps(doi_result, indent=2, ensure_ascii=False))
```

### JavaScript 示例

```javascript
const BASE_URL = 'http://localhost:8000';

// 分析文本
async function analyzeText(text, title = null) {
    const url = `${BASE_URL}/analyze/text`;
    const data = { text };
    if (title) data.title = title;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    return await response.json();
}

// 通过DOI分析
async function analyzeDOI(doi) {
    const url = `${BASE_URL}/analyze/doi`;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ doi })
    });

    return await response.json();
}

// 获取文献类型
async function getPaperTypes() {
    const url = `${BASE_URL}/paper-types`;
    const response = await fetch(url);
    return await response.json();
}

// 使用示例
(async () => {
    // 分析临床研究文本
    const clinicalText = "This randomized controlled trial...";
    const result = await analyzeText(clinicalText, "Clinical Study");
    console.log(result);

    // 分析DOI
    const doiResult = await analyzeDOI("10.1371/journal.pone.0123456");
    console.log(doiResult);
})();
```

## 错误码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误（如文本过短、DOI无效） |
| 404 | 资源未找到（如DOI无法解析） |
| 500 | 服务器内部错误 |

## 注意事项

1. 文本分析需要至少10个字符
2. DOI解析依赖网络连接，可能需要几秒钟
3. 自动提取结果仅供参考，建议人工验证
4. 建议设置合理的超时时间（建议10秒以上）
