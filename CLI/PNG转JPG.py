import os
from PIL import Image
import send2trash
import threading

# 指定包含PNG图像的目录
directory = input("请输入包含PNG图像的目录路径：")

del_confirm = input("是否删除原始PNG文件？(Y/[N]): ")

# 定义一个函数来处理单个文件的转换和删除
def process_file(filename, del_confirm):
    file_path = os.path.join(directory, filename)
    with Image.open(file_path) as img:
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            print(f'Not converting {filename} because it has transparency.')
            return

        new_filename = filename[:-4] + '.jpg'
        new_file_path = os.path.join(directory, new_filename)
        img = img.convert('RGB')
        img.save(new_file_path, 'JPEG', quality=100)
        print(f'Converted {filename} to {new_filename}')

        if del_confirm.lower() == 'y':
            send2trash.send2trash(file_path)
            print(f'Sent {filename} to trash')
        else:
            print(f'Kept original {filename}')

# 创建一个线程列表
threads = []

# 遍历目录中的所有文件
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        # 为每个文件创建一个线程
        thread = threading.Thread(target=process_file, args=(filename, del_confirm))
        threads.append(thread)
        thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

print("转换完成！")
