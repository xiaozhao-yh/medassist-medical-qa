# app.py
import os
import pickle

import faiss
import gradio as gr
from sentence_transformers import SentenceTransformer
import openai

INDEX_PATH = "faiss_index.bin"
META_PATH = "metadata.pkl"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 4

SYSTEM_PROMPT = (
    "你是一个医学知识问答助手。请基于给定的医学资料片段回答问题，"
    "并在每个关键结论后标注 [n] 来源编号。若资料中无法确定，请明确写："
    "‘资料中未覆盖，请咨询医生或专业药师。’ 本系统仅供学习参考，不构成医疗建议。"
)


def load_index():
    """加载 FAISS 索引和文档元数据."""
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        raise FileNotFoundError("未找到索引文件，请先执行 python ingest.py 建立知识库索引。")

    model = SentenceTransformer(EMBED_MODEL)
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
    return model, index, metadata


MODEL, INDEX, META = load_index()
CHUNKS = META["chunks"]
METAS = META["metas"]


def retrieve(query, top_k=TOP_K):
    q_emb = MODEL.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    distances, indices = INDEX.search(q_emb, top_k)

    results = []
    for d, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue
        results.append({
            "score": float(d),
            "text": CHUNKS[idx],
            "meta": METAS[idx],
        })
    return results


def fallback_answer(question, context):
    """无 OpenAI API key 时的简洁降级回答，仍可展示知识库内容。"""
    context_text = "\n\n".join(
        f"[{i + 1}] {item['text']}\n来源：{item['meta']['source']}"
        for i, item in enumerate(context)
    )
    answer = (
        "基于现有知识库内容，相关信息如下：\n\n"
        f"{context_text}\n\n"
        "请注意：本系统仅供学习参考，不构成医疗建议。若症状严重或反应明显，请及时就医。"
    )
    return answer


def answer_openai(question, context):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return fallback_answer(question, context)

    openai.api_key = api_key
    context_text = "\n\n".join(
        f"[{i + 1}] {item['text']}\n来源：{item['meta']['source']}"
        for i, item in enumerate(context)
    )

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"以下是检索到的知识库片段：\n{context_text}\n\n"
        f"用户问题：{question}\n\n"
        "请给出中文回答，并在关键结论后标注 [n] 来源编号。若文献不足以确认，明确说明：资料中未覆盖，请咨询医生或专业药师。"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=500,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return fallback_answer(question, context) + f"\n\n[系统说明] OpenAI 调用失败：{str(e)}"


def answer_logic(question, history, strict_mode):
    if not question or not question.strip():
        return history, history

    retrieved = retrieve(question)

    if strict_mode and not retrieved:
        reply = "根据当前知识库，无法找到足够依据的相关资料。请补充更详细的病历或咨询专业医生。"
    else:
        if not retrieved:
            reply = "当前知识库中未检索到相关资料，建议咨询医生或专业药师。"
        else:
            reply = answer_openai(question, retrieved)

    source_block = "\n\n检索来源：\n" + "\n".join(
        f"[{i + 1}] {item['meta']['title']} / {item['meta']['source']}"
        for i, item in enumerate(retrieved[:TOP_K])
    ) if retrieved else "\n\n检索来源：无"

    final_reply = reply + source_block
    new_history = history + [(question, final_reply)]
    return new_history, new_history


with gr.Blocks(title="MedAssist 医学知识问答助手") as demo:
    gr.Markdown("# 🏥 MedAssist — 医学知识问答助手")
    gr.Markdown("> 本系统仅供学习参考，不构成医疗建议。若出现急性病情，请及时就医。")

    chatbot = gr.Chatbot(type="messages")
    txt = gr.Textbox(placeholder="例如：阿司匹林有哪些常见副作用？")
    strict = gr.Checkbox(label="严格模式：仅基于知识库内容回答", value=True)
    send = gr.Button("发送")

    def submit(user_message, history, strict_mode):
        if not user_message or not user_message.strip():
            return history, history
        return answer_logic(user_message, history or [], strict_mode)

    send.click(submit, [txt, chatbot, strict], [chatbot, chatbot])
    txt.submit(submit, [txt, chatbot, strict], [chatbot, chatbot])

if __name__ == "__main__":
    demo.launch()
