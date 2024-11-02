import os
import re

def find_empty_directories(directory, regex_pattern):
    empty_dirs = []
    pattern = re.compile(regex_pattern)
    for root, dirs, files in os.walk(directory, topdown=False):
        if not dirs and not files:
            if pattern.search(root):
                empty_dirs.append(root)
    return empty_dirs

def delete_empty_directories(empty_dirs):
    for dir in empty_dirs:
        os.rmdir(dir)
        print(f"已删除空文件夹: {dir}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_directory = script_dir
    default_regex_pattern = ".*"  # 默认匹配所有文件夹
    print(f"目录默认值是脚本所在目录: {default_directory}")
    print(f"正则表达式默认值是: {default_regex_pattern}")

    directory = input(f"请输入要删除空文件夹的目录路径 (默认: {default_directory}): ")
    directory = directory if directory else default_directory

    regex_pattern = input(f"请输入正则表达式来筛选空文件夹 (默认: {default_regex_pattern}): ")
    regex_pattern = regex_pattern if regex_pattern else default_regex_pattern

    empty_dirs = find_empty_directories(directory, regex_pattern)

    if empty_dirs:
        print("找到以下匹配的空文件夹:")
        for dir in empty_dirs:
            print(dir)
        confirmation = input("是否删除这些空文件夹？(y/n): ")
        if confirmation.lower() == 'y':
            delete_empty_directories(empty_dirs)
            print("空文件夹已删除。")
        else:
            print("操作已取消。")
    else:
        print("没有找到匹配的空文件夹。")

if __name__ == "__main__":
    main()
