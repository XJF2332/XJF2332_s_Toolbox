import json

import charset_normalizer

json_path = input("请输入json文件路径：")

with open(json_path, 'rb') as file:
    content_bytes = file.read()

encoding_info = charset_normalizer.detect(content_bytes)
print("检测到的编码信息：", encoding_info)
encoding = encoding_info['encoding'] if encoding_info else 'utf-8'

with open(json_path, 'r', encoding=encoding) as f:
    doc = json.load(f)

sorted_doc = dict(sorted(doc.items()))

with open(json_path, 'w',encoding="utf-8") as f:
    json.dump(sorted_doc, f, ensure_ascii=False, indent=4)

print("JSON 文件已排序，文件已保存到原文件")
