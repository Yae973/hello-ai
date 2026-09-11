import re
import jieba
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Hello-AI",
    page_icon="🤖",
    layout="wide"
)
st.markdown("""
<style>

html, body, [class*="css"] {
    color:#1f2937;
}

.stApp {
    background:#fafafa;
}


/* sidebar */

[data-testid="stSidebar"] {
    background:#f4f5f7;
}


[data-testid="stSidebar"] * {
    color:#374151;
}


/* 标题 */

.title {
    font-size:52px;
    font-weight:600;
    color:#111827;
}


.subtitle {
    font-size:20px;
    color:#6b7280;
}



/* 卡片 */

.card {

background:white;

padding:28px;

border-radius:24px;

box-shadow:
0 10px 30px rgba(0,0,0,0.06);

color:#111827;

}


/* 输入框 */

[data-testid="stChatInput"] {

background:white;

border-radius:30px;

}


</style>
""", unsafe_allow_html=True)

# 样式
st.markdown("""
<style>

body {
    background:#fafafa;
}

.main {
    background:#fafafa;
}

/* 左侧菜单 */
[data-testid="stSidebar"] {
    background:#f5f6f8;
}

/* 标题 */
.title {
    font-size:48px;
    font-weight:600;
    color:#111827;
    margin-top:50px;
}

.subtitle {
    font-size:20px;
    color:#64748b;
}

/* 卡片 */
.card {
    background:white;
    padding:25px;
    border-radius:22px;
    box-shadow:0 5px 25px rgba(0,0,0,0.05);
    height:120px;
}

/* 输入框 */
.stChatInput {
    border-radius:30px;
}

</style>
""", unsafe_allow_html=True)


# 左侧
with st.sidebar:

    st.markdown("""
    # Hello-AI

    你的知识库助手
    """)

    st.divider()

    st.button("💬 对话")
    st.button("📚 知识库")
    st.button("⬆ 上传文件")
    st.button("⚙ 设置")

    st.divider()

    st.caption("知识库")
    st.write("📁 全部文件")
    st.write("📁 编程开发")
    st.write("📁 AI资料")


# 主页面

st.markdown(
    '<div class="title">Hello-AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">基于你的知识，给你更准确、更有价值的回答</div>',
    unsafe_allow_html=True
)


st.write("")


c1,c2,c3 = st.columns(3)


with c1:
    st.markdown("""
    <div class="card">
    📚<br>
    <b>专属知识库</b><br>
    基于你的资料回答
    </div>
    """,unsafe_allow_html=True)


with c2:
    st.markdown("""
    <div class="card">
    ⚡<br>
    <b>快速检索</b><br>
    精准找到内容
    </div>
    """,unsafe_allow_html=True)


with c3:
    st.markdown("""
    <div class="card">
    🔒<br>
    <b>隐私安全</b><br>
    数据只属于你
    </div>
    """,unsafe_allow_html=True)



st.write("")


# 对话区域

if "messages" not in st.session_state:
    st.session_state.messages=[]


for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(
            f"<div style='color:#111827; font-size:18px;'>{m['content']}</div>",
            unsafe_allow_html=True
        )

        if m["role"] == "assistant" and m.get("sources"):
            st.markdown(
    f"<div style='color:#6b7280; font-size:14px; margin-top:6px;'>来源：{m['sources']}</div>",
    unsafe_allow_html=True
)


question = st.chat_input(
    "输入你的问题..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    knowledge_dir = Path("knowledge")

    results = []

    for file in knowledge_dir.glob("*.txt"):
        text = file.read_text(encoding="utf-8")

    for line in text.splitlines():            
        q = [word.strip().lower() for word in jieba.cut(question) if word.strip()]
        l = [word.strip().lower() for word in jieba.cut(line) if word.strip()]

        stop_words = {"是", "的", "和", "了", "吗", "呢", "啊", "怎么", "什么", "干什么", "用来"}

        q = [word for word in q if word not in stop_words]

        score = 0

        for word in q:
            if word in l or any(word in item for item in l):
                score += 1

        if score >= 1:
            results.append(
        {
            "score": score,
            "text": line,
            "source": file.name
        }
    )
    
    if results:
        results.sort(
            key=lambda item: item["score"],
            reverse=True
    )

        best = results[0]

        answer = best["text"]
        sources = best["source"]

    else:
        answer = "知识库中没有找到相关内容。"
        sources = ""
    
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )

    st.rerun()