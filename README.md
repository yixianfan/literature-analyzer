# 文献整理在线工具

一个基于Python的文献整理在线工具，自动识别文献类型并提取结构化信息，对标Paper-DeepReader-v2.0。

## 📋 功能特点

- **文献类型自动识别**：支持临床研究、病例报告、基础研究三种类型
- **结构化信息提取**：按照期刊标准模板提取关键信息
- **DOI解析**：支持通过DOI链接自动获取文献信息
- **API接口**：基于FastAPI的RESTful API，支持多种调用方式
- **异常处理**：完善的错误处理和验证机制

## 🔧 工具工作流程

1. **输入接收**：接收文献文本或DOI链接
2. **类型识别**：基于关键词和模式匹配自动识别文献类型
3. **模板匹配**：根据文献类型选择对应的结构化模板
4. **信息提取**：使用正则表达式和NLP技术提取关键信息
5. **结果输出**：返回JSON格式的结构化分析报告

## 📁 项目结构

```
literature_analyzer/
├── main.py                    # FastAPI主程序
├── requirements.txt           # 依赖包列表
├── modules/                   # 核心模块
│   ├── __init__.py
│   ├── paper_classifier.py    # 文献类型识别器
│   ├── doi_resolver.py        # DOI解析器
│   └── info_extractor.py      # 信息提取器
├── templates/                 # 结构化模板
│   ├── __init__.py
│   ├── clinical_template.py   # 临床研究模板（8大模块）
│   ├── case_template.py       # 病例报告模板（5大模块）
│   └── basic_template.py      # 基础研究模板（5大模块）
├── tests/                     # 测试用例
│   ├── test_classifier.py
│   ├── test_doi_resolver.py
│   ├── test_templates.py
│   └── test_api.py
└── docs/                      # 文档
    └── API.md
```

## 🚀 安装与部署

### 环境要求

- Python 3.8+
- 网络连接（用于DOI解析）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd literature_analyzer
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **启动服务**
```bash
python main.py
```

或使用uvicorn：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

5. **访问API文档**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📖 API 接口文档

### 1. 根路径
```
GET /
```
返回API基本信息。

### 2. 健康检查
```
GET /health
```
检查服务状态。

### 3. 获取支持的文献类型
```
GET /paper-types
```
返回支持的文献类型及其模块定义。

### 4. 分析文本
```
POST /analyze/text
Content-Type: application/json

{
    "text": "文献全文或摘要文本",
    "title": "文献标题（可选）"
}
```

### 5. 通过DOI分析
```
POST /analyze/doi
Content-Type: application/json

{
    "doi": "DOI字符串或DOI链接"
}
```

## 💻 API 调用示例

### 使用 curl

**分析文献文本**
```bash
curl -X POST "http://localhost:8000/analyze/text" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "This randomized controlled trial evaluated a new treatment in 100 patients with diabetes. The intervention group showed significant improvement (p<0.001).",
       "title": "Diabetes Treatment Study"
     }'
```

**通过DOI分析**
```bash
curl -X POST "http://localhost:8000/analyze/doi" \
     -H "Content-Type: application/json" \
     -d '{"doi": "10.1000/xyz123"}'
```

**获取支持的文献类型**
```bash
curl -X GET "http://localhost:8000/paper-types"
```

### 使用 Python requests

```python
import requests

# 分析文本
url = "http://localhost:8000/analyze/text"
data = {
    "text": "This randomized controlled trial evaluated...",
    "title": "Study Title"
}
response = requests.post(url, json=data)
result = response.json()
print(result)

# 分析DOI
url = "http://localhost:8000/analyze/doi"
data = {"doi": "10.1000/xyz123"}
response = requests.post(url, json=data)
result = response.json()
print(result)
```

### 使用 JavaScript fetch

```javascript
// 分析文本
fetch('http://localhost:8000/analyze/text', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: '文献文本内容...',
        title: '文献标题'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📊 输出格式

### 响应示例
```json
{
    "paper_type": "clinical_research",
    "paper_type_description": "临床研究",
    "confidence": 0.85,
    "core_info": {
        "background": "研究背景信息...",
        "objective": "研究目的...",
        "methods": "研究方法...",
        "participants": "研究对象...",
        "intervention": "干预措施...",
        "outcomes": "结局指标...",
        "results": "研究结果...",
        "conclusion": "结论..."
    },
    "full_analysis": {
        "paper_type": "clinical_research",
        "modules": { ... },
        "classification": { ... },
        "metadata": { ... }
    },
    "generation_time": "2025-12-14 17:02:00"
}
```

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_classifier.py

# 运行测试并显示覆盖率
pytest --cov=modules --cov=templates
```

## 📝 文献类型说明

### 1. 临床研究（clinical_research）
**参考标准**：Lancet期刊结构（8大模块）
- **研究背景**：疾病背景和研究意义
- **研究目的**：研究要解决的具体问题
- **研究方法**：研究设计和实施方法
- **研究对象**：受试者特征和纳入标准
- **干预措施**：实验组和对照组的处理
- **结局指标**：主要和次要终点
- **研究结果**：主要发现和统计数据
- **结论**：研究结论和临床意义

### 2. 病例报告（case_report）
**参考标准**：Blood期刊结构（5大模块）
- **病例概述**：患者基本信息和病史
- **临床表现**：症状、体征和检查结果
- **诊断过程**：诊断思路和检查发现
- **治疗方案**：治疗措施和用药情况
- **治疗结果**：疗效和随访情况

### 3. 基础研究（basic_research）
**标准结构**（5大模块）
- **科学问题**：要解决的科学问题或研究空白
- **研究方法**：实验设计、材料和方法
- **研究结果**：实验数据和主要发现
- **研究结论**：主要结论和意义
- **作用机制**：分子机制和信号通路

## 🔍 技术实现

### 文献类型识别
- 基于关键词加权评分
- 支持中英文关键词
- 动态置信度计算

### 信息提取
- 正则表达式模式匹配
- 结构化模板提取
- 多层次兜底策略

### DOI解析
- CrossRef API集成
- PubMed API备用
- 元数据标准化

## ⚠️ 注意事项

1. **网络依赖**：DOI解析需要网络连接
2. **文本长度**：建议文本长度至少100字符
3. **DOI有效性**：确保DOI链接可访问
4. **结果准确性**：自动提取结果仅供参考，需人工验证

## 🛠️ 扩展开发

### 添加新的文献类型
1. 在`paper_classifier.py`中添加关键词
2. 创建对应的模板文件
3. 在`info_extractor.py`中注册模板

### 改进识别算法
- 集成机器学习模型
- 添加更多特征提取
- 优化权重计算

### 增强DOI解析
- 添加更多数据源API
- 实现全文抓取
- 支持批量处理

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题，请提交Issue或联系开发团队。
