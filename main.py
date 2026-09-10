from pathlib import Path

file_path = Path("knowledge/test.txt")
content = file_path.read_text(encoding="utf-8")

question = input("请输入你想查询的关键词：")

print("\n=== 搜索结果 ===")

found = False

for line in content.splitlines():
    if question.lower() in line.lower():
        print(line)
        found = True

if not found:
    print("知识库中没有找到相关内容。")