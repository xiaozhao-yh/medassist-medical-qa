# MedAssist

MedAssist 是一个基于 RAG 的医学知识问答助手，适用于课程实验和教学演示。系统支持：

- 基于知识库问答（药品、疾病、适应症、禁忌症、用法用量等）
- 结合前端界面进行交互式问答
- 文档入库与 RAG 检索
- 严格模式：只基于知识库内容回答
- 注明“仅供学习参考，不构成医疗建议”

## 1. 功能概览

- 自由问答：用户输入任意医学问题
- 药品快速查询：按药品名进行针对性问答
- RAG 检索：将问答基于知识库文档进行检索和生成
- 多轮上下文：支持简易对话历史上下文
- 安全提示：界面内置医疗免责声明
- 可扩展：支持上传 PDF / TXT 文档进一步扩充知识库

## 2. 项目结构

```text
medassist/
├── app.py
├── ingest.py
├── utils.py
├── requirements.txt
├── README.md
├── docs/
│   ├── sample_drug_info.txt
│   └── sample_disease_info.txt
├── faiss_index.bin
├── metadata.pkl
└── .env.example
```

## 3. 运行环境

- Python 3.10+
- CPU/GPU 均可
- 推荐：Windows/Linux/macOS

## 4. 安装依赖

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
# 或 venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## 5. 准备知识库数据

将医学资料文本（TXT/PDF）放入 `docs/` 目录中，示例已包含：

- `sample_drug_info.txt`
- `sample_disease_info.txt`

## 6. 建立索引

```bash
python ingest.py
```

这一步会读取 `docs/` 中的内容，构建 FAISS 索引和文档元数据。若你想重新建立索引，可删除旧索引文件后再执行。

## 7. 启动应用

```bash
python app.py
```

程序启动后，浏览器访问 Gradio 提供的本地 URL，例如：

```text
http://127.0.0.1:7860/
```

## 8. 使用说明

- 在输入框中提问，例如：
  - 阿司匹林有哪些常见副作用？
  - 甲氨蝶呤禁忌症有哪些？
  - 感冒和发烧应该怎么处理？
- 勾选“严格模式”后，系统会只基于知识库中内容回答。
- 界面下方会展示检索到的来源信息。

## 9. 免责声明

> 本系统仅供学习、教学和研究参考，不构成医疗建议。任何疾病或药物使用问题均应咨询具备资质的医疗专业人员。紧急情况请尽快前往医院或拨打急救电话。

## 10. 实验报告建议

可在实验报告中写明：

1. 项目背景与目标
2. 系统架构设计
3. RAG 检索原理
4. 多轮对话与限制
5. 测试问题与结果分析
6. 存在问题与改进方案

## 11. 扩展方向

- 接入真实药品说明书与诊疗资料
- 加入文档上传功能（PDF / DOCX）
- 改进检索质量（重排、分块策略）
- 接入国产大模型（Qwen / GLM）
- 加入日志记录、用户反馈和知识库管理功能

## 12. 许可证

MIT License

