# ingest.py
import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss

from utils import load_plain_texts_from_dir, chunk_text

EMBED_MODEL = "all-MiniLM-L6-v2"
INDEX_PATH = "faiss_index.bin"
META_PATH = "metadata.pkl"
DOC_DIR = "docs"


def build_index():
    print("加载模型...")
    model = SentenceTransformer(EMBED_MODEL)

    print("读取文档...")
    docs = load_plain_texts_from_dir(DOC_DIR)

    chunks = []
    metas = []

    for doc in docs:
        for idx, chunk in enumerate(chunk_text(doc["text"], max_chars=800, overlap=100)):
            chunks.append(chunk)
            metas.append({
                "doc_id": doc["id"],
                "title": doc.get("title", ""),
                "source": doc.get("source", ""),
                "chunk_index": idx,
            })

    print(f"共 {len(chunks)} 个文本片段，开始 embedding...")
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump({"chunks": chunks, "metas": metas}, f)

    print("索引构建完成。")


if __name__ == "__main__":
    if not os.path.exists(DOC_DIR):
        print(f"未找到文档目录: {DOC_DIR}，请先创建并放入知识库文件。")
        raise SystemExit(1)
    build_index()
