import os
from PIL import Image
import send2trash
import threading

# 指定包含PNG图像的目录
directory = input("请输入包含PNG图像的目录路径：")
del_confirm = input("是否删除原始PNG文件？(Y/[N]): ")
quality = input("请输入JPEG图像的质量（1-[100]）：")
transparency_trans = input("是否转换含有透明度的图像？(Y/[N]): ")

if quality:
    try:
        if int(quality) < 1 or int(quality) > 100:
            raise ValueError
        else:
            quality = int(quality)
    except ValueError:
        print("无效的质量值，使用默认值100")
        quality = 100
else:
    quality = 100

if transparency_trans.lower() == 'y':
    transparency_trans = True
else:
    transparency_trans = False

# 定义一个函数来处理单个文件的转换和删除
def process_file(filename, del_confirm):
    global quality
    file_path = os.path.join(directory, filename)
    with Image.open(file_path) as img:
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            if transparency_trans:
                print(f'{filename} 含有透明度，但由于自定义设置仍然进行转换')
            else:
                print(f'跳过 {filename} ，因为它含有透明度')
                return

        new_filename = filename[:-4] + '.jpg'
        new_file_path = os.path.join(directory, new_filename)
        img = img.convert('RGB')
        img.save(new_file_path, 'JPEG', quality=quality)
        print(f'成功转换 {filename} 为 {new_filename}')

        if del_confirm.lower() == 'y':
            send2trash.send2trash(file_path)
            print(f'已将 {filename} 发送到回收站')
        else:
            print(f'保留原文件：{filename}')

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
