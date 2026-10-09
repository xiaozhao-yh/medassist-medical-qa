# MedAssist 医学知识问答助手

MedAssist 是一个面向课程实验的医学知识问答系统，采用“知识库 + RAG 检索 + 大模型生成”的方式，实现医药类问答、疾病咨询、药品常识查询等功能。项目面向教学演示，适合作为《AI大模型原理与应用》实验四的扩展项目。

## 项目功能

- 自由问答：输入任意医学/药品/健康相关问题
- 药品知识查询：支持专门按药品名查询
- 疾病常识问答：支持常见疾病症状、处理建议等
- RAG 检索：先从知识库中找出相关段落，再调用大模型生成答案
- 严格模式：只基于知识库内容回答，不扩展未检索到的信息
- 多轮对话：支持简易历史上下文
- 安全提示：界面内置医疗说明，明确仅供学习参考

## 运行环境

- Python 3.10+
- CPU 或 GPU
- 可选：OpenAI API Key（推荐）

## 项目结构

```text
medassist-medical-qa/
├── app.py
├── ingest.py
├── utils.py
├── requirements.txt
├── README.md
├── .env.example
├── docs/
│   ├── sample_drug_info.txt
│   └── sample_disease_info.txt
├── faiss_index.bin
├── metadata.pkl
└── .gitignore
```

## 安装依赖

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
# 或 venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## 建立知识库索引

```bash
python ingest.py
```

若 `docs/` 下没有文件，需要先放入知识库文档，例如 `.txt` 或 `.pdf` 文件。

## 启动应用

```bash
python app.py
```

启动后访问 Gradio 提供的本地地址，例如：

```text
http://127.0.0.1:7860/
```

## 示例问题

- 阿司匹林有哪些常见副作用？
- 甲氨蝶呤的禁忌症有哪些？
- 普通感冒能否使用抗生素？
- 发烧时应该注意哪些情况？

## 免责声明

> 本系统仅供学习和教学参考，不构成医疗建议。任何疾病或药物使用问题请咨询专业医生；如果出现严重症状，应及时就医。

## 实验报告写作建议

1. 项目背景与需求分析
2. 系统架构设计
3. RAG 检索流程说明
4. 大模型提示词设计
5. 测试案例与结果分析
6. 存在问题与改进方向

## 扩展方向

- 增加 PDF / DOCX 批量上传功能
- 接入更强大的国产大模型（Qwen / GLM）
- 优化 RAG 检索与重排策略
- 增加日志、追踪、用户反馈和知识库管理

## 许可证

MIT License
