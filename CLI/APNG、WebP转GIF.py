import os
import sys
from PIL import Image
import send2trash
from tqdm import tqdm
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import filedialog

def is_apng(file_path):
    try:
        with Image.open(file_path) as img:
            return img.is_animated and img.format == 'PNG'
    except Exception:
        return False

def is_animated_webp(file_path):
    try:
        with Image.open(file_path) as img:
            return img.is_animated and 'webp' in img.format.lower()
    except Exception:
        return False

def get_file_list(root_dir, recursive=False):
    file_list = []
    if recursive:
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.lower().endswith(('.apng', '.png', '.webp')):
                    file_list.append(file_path)
    else:
        for file in os.listdir(root_dir):
            file_path = os.path.join(root_dir, file)
            if os.path.isfile(file_path) and file_path.lower().endswith(('.apng', '.png', '.webp')):
                file_list.append(file_path)
    return file_list

def convert_to_gif(input_path, output_path, quality=None):
    try:
        with Image.open(input_path) as img:
            if img.is_animated or (img.format == 'PNG' and getattr(img, 'n_frames', 1) > 1):
                img.save(output_path, 'GIF', save_all=True, optimize=True, quality=quality)
                return True
            else:
                tqdm.write(f"Skipping {input_path} as it's not an animated image.")
                return False
    except Exception as e:
        tqdm.write(f"Error converting {input_path}: {e}")
        return False

def main():
    # 获取用户输入的目录路径
    user_input = input("请输入目录路径或输入 ---dialog 选择目录: ")
    if user_input == '---dialog':
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        root_dir = filedialog.askdirectory()
        if not root_dir:
            print("未选择目录。")
            sys.exit(1)
        else:
            print(f"选择的目录是: {root_dir}")
    else:
        root_dir = user_input
    if not os.path.isdir(root_dir):
        print("无效的目录路径。")
        sys.exit(1)

    # 询问是否递归遍历目录
    recursive_input = input("是否递归遍历目录? (Y/[N]) ").strip().lower()
    recursive = recursive_input == 'y'

    # 询问是否发送原文件到回收站
    send_to_trash_input = input("是否发送原文件到回收站? (Y/[N]) ").strip().lower()
    send_to_trash = send_to_trash_input == 'y'

    # 询问GIF质量
    quality_input = input("请输入GIF质量（留空为自动设置）: ").strip()
    if quality_input:
        try:
            quality = int(quality_input)
        except ValueError:
            print("质量值无效，使用自动设置。")
            quality = None
    else:
        quality = None

    # 获取文件列表
    file_list = get_file_list(root_dir, recursive)
    if not file_list:
        print("没有找到符合条件的文件。")
        sys.exit(0)

    # 转换文件并显示进度条
    for file_path in tqdm(file_list, desc="转换进度", unit="文件"):
        if not is_apng(file_path) and not is_animated_webp(file_path):
            continue

        output_path = os.path.splitext(file_path)[0] + '.gif'
        if os.path.exists(output_path):
            tqdm.write(f"跳过转换 {file_path}，因为 {output_path} 已经存在。")
            continue

        if convert_to_gif(file_path, output_path, quality=quality):
            if send_to_trash:
                send2trash.send2trash(file_path)
                tqdm.write(f"已将 {file_path} 发送到回收站。")

    # 显示任务完成通知
    toaster = ToastNotifier()
    toaster.show_toast("转换完成", "所有文件已转换完成！", duration=5)

if __name__ == "__main__":
    main()