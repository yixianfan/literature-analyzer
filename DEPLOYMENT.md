# 🚀 GitHub 部署指南

## ✅ 已完成部署

您的文献整理工具已成功部署到GitHub！

**仓库地址**: https://github.com/yixianfan/literature-analyzer

### 📊 部署信息
- **分支**: master (已推送)
- **分支**: main (已推送)
- **文件数**: 21个文件
- **代码行数**: 2851行

## 📝 下一步设置

### 1. 设置默认分支为main（推荐）

现代GitHub项目默认使用`main`分支作为主分支。请按以下步骤操作：

1. 访问 https://github.com/yixianfan/literature-analyzer
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **General**
4. 滚动到 **Default branch** 部分
5. 点击下拉菜单，选择 **main**
6. 点击 **Update** 按钮确认

### 2. 配置GitHub Pages（可选）

如果您想在GitHub Pages上部署演示版本：

1. 进入仓库 **Settings** 页面
2. 找到 **Pages** 标签
3. 在 **Source** 下选择分支（建议创建一个 `gh-pages` 分支用于演示）

### 3. 创建Release版本

1. 进入仓库 **Releases** 页面
2. 点击 **Create a new release**
3. 填写版本号（如 `v1.0.0`）
4. 添加发布说明
5. 点击 **Publish release**

## 📁 仓库结构

```
literature-analyzer/
├── README.md              # 项目说明文档
├── QUICKSTART.md          # 快速开始指南
├── DEPLOYMENT.md          # 本文件（部署说明）
├── requirements.txt       # Python依赖
├── main.py               # FastAPI应用主程序
├── start_server.py       # 服务器启动脚本
├── examples.py           # 使用示例
├── run_tests.py          # 测试运行脚本
├── modules/              # 核心模块
│   ├── paper_classifier.py
│   ├── doi_resolver.py
│   └── info_extractor.py
├── templates/            # 结构化模板
│   ├── clinical_template.py
│   ├── case_template.py
│   └── basic_template.py
├── tests/                # 测试用例
│   ├── test_api.py
│   ├── test_classifier.py
│   ├── test_doi_resolver.py
│   └── test_templates.py
└── docs/                 # 详细文档
    └── API.md
```

## 🔧 克隆和本地开发

```bash
# 克隆仓库
git clone https://github.com/yixianfan/literature-analyzer.git
cd literature-analyzer

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python start_server.py

# 运行测试
python run_tests.py
```

## 📋 后续维护

### 添加新功能

1. 创建功能分支
```bash
git checkout -b feature/new-feature
```

2. 提交更改
```bash
git add .
git commit -m "Add new feature"
```

3. 推送到GitHub
```bash
git push origin feature/new-feature
```

4. 创建Pull Request

### 更新文档

文档文件列表：
- `README.md` - 项目主页说明
- `QUICKSTART.md` - 快速开始指南
- `docs/API.md` - API详细文档
- `DEPLOYMENT.md` - 部署说明（本文件）

### 发布新版本

1. 更新版本号（在适当位置）
2. 更新 `CHANGELOG.md`（建议创建）
3. 创建新的 Release
4. 推送标签
```bash
git tag v1.1.0
git push origin v1.1.0
```

## 🌟 项目亮点

### 功能特性
- ✅ 自动文献类型识别（临床研究、病例报告、基础研究）
- ✅ 结构化信息提取（参考顶级期刊标准）
- ✅ DOI解析和元数据获取
- ✅ RESTful API（FastAPI）
- ✅ 完整单元测试覆盖
- ✅ 详细文档和示例

### 技术栈
- **后端**: Python 3.8+, FastAPI, uvicorn
- **文本处理**: nltk, regex
- **测试**: pytest
- **文档**: Markdown

## 📞 支持

如果您在使用过程中遇到问题：

1. 查看项目文档 (`README.md`, `QUICKSTART.md`)
2. 查看API文档 (`docs/API.md`)
3. 运行测试检查问题 (`python run_tests.py`)
4. 提交Issue到GitHub仓库

## 🎯 下一步计划

- [ ] 添加Docker部署支持
- [ ] 集成更多DOI数据源
- [ ] 支持批量文献分析
- [ ] 添加Web UI界面
- [ ] 性能优化和缓存

## 🎉 恭喜！

您的文献整理在线工具已成功部署到GitHub！

访问链接：https://github.com/yixianfan/literature-analyzer

开始使用吧！ 🚀
