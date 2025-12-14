# 快速开始指南

## 🚀 快速启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务
```bash
python start_server.py
```

或使用uvicorn：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问服务
- **API文档**: http://localhost:8000/docs
- **交互式测试**: 在浏览器中打开Swagger UI

## 📝 快速测试

### 测试文本分析
```bash
python examples.py
```

### 运行单元测试
```bash
python run_tests.py
```

## 💡 使用示例

### 分析文献文本
```python
import requests

url = "http://localhost:8000/analyze/text"
data = {
    "text": "This randomized controlled trial evaluated...",
    "title": "Study Title"
}
response = requests.post(url, json=data)
print(response.json())
```

### 通过DOI分析
```python
import requests

url = "http://localhost:8000/analyze/doi"
data = {"doi": "10.1371/journal.pone.0123456"}
response = requests.post(url, json=data)
print(response.json())
```

## 📚 了解更多

- **详细文档**: 查看 [README.md](README.md)
- **API文档**: 查看 [docs/API.md](docs/API.md)
- **示例代码**: 查看 [examples.py](examples.py)

## ❓ 常见问题

### Q: 如何修改端口？
A: 编辑 `start_server.py` 或使用命令行参数：
```bash
uvicorn main:app --port 9000
```

### Q: DOI解析失败怎么办？
A: 检查网络连接，确保DOI有效。部分文献可能需要订阅才能获取全文。

### Q: 如何添加新的文献类型？
A: 参考 `templates/` 目录下的模板文件，创建新的模板并在 `info_extractor.py` 中注册。

## 🛠️ 开发指南

### 项目结构
```
literature_analyzer/
├── main.py                 # FastAPI应用
├── modules/                # 核心模块
│   ├── paper_classifier.py
│   ├── doi_resolver.py
│   └── info_extractor.py
├── templates/              # 结构化模板
│   ├── clinical_template.py
│   ├── case_template.py
│   └── basic_template.py
├── tests/                  # 测试用例
└── docs/                   # 文档
```

### 添加新功能
1. 在相应模块中添加代码
2. 编写测试用例
3. 更新文档

## 📞 支持

如有问题，请：
1. 查看详细文档 [README.md](README.md)
2. 查看API文档 [docs/API.md](docs/API.md)
3. 运行测试检查问题 [run_tests.py](run_tests.py)
