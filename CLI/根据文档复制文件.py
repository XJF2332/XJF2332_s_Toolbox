import shutil
import os
from concurrent.futures import ThreadPoolExecutor

# input txt path
txt_path = input("请输入txt文件路径：")

temp_path = "temp"

if not os.path.exists(temp_path):
    os.makedirs(temp_path)

# function to copy file
def copy_file(file_name):
    if os.path.exists(file_name):
        shutil.copy(file_name, temp_path)
        print(f"已复制文件：{file_name} 到 {temp_path}")
    elif not os.path.isfile(file_name):
        print(f"不是文件：{file_name}")
    else:
        print(f"文件不存在：{file_name}")

# read every line in txt
with open(txt_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# create a thread pool with a maximum of 5 threads
with ThreadPoolExecutor(max_workers=5) as executor:
    # submit tasks to the thread pool
    for line in lines:
        file_name = line.strip()
        executor.submit(copy_file, file_name)

print("所有文件复制完成。")
