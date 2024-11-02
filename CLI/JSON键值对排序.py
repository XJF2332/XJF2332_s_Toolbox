import json

json_path = input("请输入json文件路径：")

# 读取 JSON 文件
with open(json_path, 'r',encoding="utf-8") as f:
    doc = json.load(f)

 # 对 JSON 文件中的键值对进行排序
sorted_doc = dict(sorted(doc.items()))

# 将排序后的 JSON 文件写入源文件
with open(json_path, 'w',encoding="utf-8") as f:
    json.dump(sorted_doc, f, ensure_ascii=False, indent=4)

print("JSON 文件已排序")

