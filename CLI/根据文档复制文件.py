import os
import shutil
from concurrent.futures import ThreadPoolExecutor

import charset_normalizer

txt_path = input("请输入txt文件路径：")
temp_path = "temp"

if not os.path.exists(temp_path):
    os.makedirs(temp_path)

def copy_file(file_name):
    if os.path.exists(file_name):
        shutil.copy(file_name, temp_path)
        print(f"已复制文件：{file_name} 到 {temp_path}")
    elif not os.path.isfile(file_name):
        print(f"不是文件：{file_name}")
    else:
        print(f"文件不存在：{file_name}")

with open(txt_path, 'rb') as file:
    content_bytes = file.read()

encoding_info = charset_normalizer.detect(content_bytes)
print("检测到的编码信息：", encoding_info)
encoding = encoding_info['encoding'] if encoding_info else 'utf-8'

with open(txt_path, 'r', encoding=encoding) as f:
    lines = f.readlines()

with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    for line in lines:
        file_name = line.strip()
        executor.submit(copy_file, file_name)

print("所有文件复制完成。")
