# 🚀 crop_pdf_fast.py – 高性能 PDF 页面裁剪工具

`crop_pdf_fast.py` 是一个基于 **pikepdf（C++ qpdf 引擎）** 的高性能 PDF 裁剪脚本。  
它支持从大型 PDF 中：

- 按页范围截取
- 裁剪起始页的底部百分比
- 裁剪终止页的顶部百分比
- 完整的短参数、长参数支持（例如：`-i|--input`）

特别适合处理数千页的大型文档，如技术规范、PRM、操作手册等。

---

## ✨ 功能特性

### 🔹 页范围裁剪
- `--start-page N` 从第 N 页开始（默认 1）
- `--end-page M` 截止到第 M 页（默认最后一页）

### 🔹 百分比裁剪
- `--start-bottom-pct 40` → 起始页保留底部 40%
- `--end-top-pct 30` → 终止页保留顶部 30%

### 🔹 高性能
使用 `pikepdf`（基于 C++ 的 qpdf），比 PyPDF2/pypdf 更快，适合超大 PDF。

### 🔹 参数依赖检查
脚本自动校验参数合法性，防止冲突或误操作。

### 🔹 完整 `-h|--help` 支持
提供详细帮助与示例。

---

## 📦 安装依赖

```bash
pip install pikepdf
