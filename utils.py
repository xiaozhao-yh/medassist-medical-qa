# utils.py
import os
import glob
import uuid

import pdfplumber


def load_plain_texts_from_dir(dirpath):
    """解析目录中的文本文件和 PDF，返回结构化文档列表"""
    items = []
    for p in glob.glob(os.path.join(dirpath, "*")):
        name = os.path.basename(p)
        doc_id = str(uuid.uuid4())

        if p.lower().endswith(".pdf"):
            try:
                with pdfplumber.open(p) as pdf:
                    text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            except Exception as e:
                print(f"PDF解析失败: {p}，错误：{e}")
                continue
        elif p.lower().endswith(".txt"):
            with open(p, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            continue

        items.append({
            "id": doc_id,
            "title": name,
            "source": p,
            "text": text,
        })

    return items


def chunk_text(text, max_chars=800, overlap=100):
    """简单按字符长度分块，保留一定重叠"""
    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)
        chunks.append(text[start:end])
        start = max(end - overlap, end)

    return chunks
