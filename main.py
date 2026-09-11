from dotenv import load_dotenv
import os
from openai import OpenAI
from pathlib import Path


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# 读取知识库
knowledge = Path("knowledge/test.txt").read_text(
    encoding="utf-8"
)


question = input("请输入问题：")


prompt = f"""
你是一个知识库助手。

请根据下面资料回答问题。

知识库：
{knowledge}


问题：
{question}

如果资料没有答案，请说：
知识库中没有相关信息。
"""


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


print("\n=== AI回答 ===")
print(response.choices[0].message.content)