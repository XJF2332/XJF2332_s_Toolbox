import os
import re
import send2trash
import sys

def find_files(directory, pattern, recursive=True, match_full_path=True):
    """查找匹配正则表达式的文件"""
    matching_files = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if match_full_path:
                    filepath = os.path.join(root, file)
                else:
                    filepath = file
                if pattern.search(filepath):
                    matching_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                if match_full_path:
                    filepath = os.path.join(directory, file)
                else:
                    filepath = file
                if pattern.search(filepath):
                    matching_files.append(os.path.join(directory, file))
    return matching_files


def main():
    print("输入'---quit'以停止脚本。")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_directory = script_dir
    current_regex_pattern = ".+"
    pattern = re.compile(current_regex_pattern)

    while True:
        # 输入目录
        directory_change = input(f"请输入目录路径 (当前: {current_directory}): ")
        if directory_change == "---quit":
            print("脚本已停止。")
            break
        if directory_change:
            if not os.path.isdir(directory_change):
                print("目录不存在，请重新输入。")
                continue
            current_directory = directory_change
        else:
            print(f"使用当前目录：{current_directory}")

        # 输入正则表达式
        regex_pattern_change = input(f"请输入正则表达式 (当前: {current_regex_pattern}): ")
        if regex_pattern_change == "---quit":
            print("脚本已停止。")
            break
        if regex_pattern_change:
            try:
                pattern = re.compile(regex_pattern_change)
                current_regex_pattern = regex_pattern_change
            except re.error as e:
                print(f"正则表达式编译错误：{e}")
                continue
        else:
            print(f"使用当前正则表达式：{current_regex_pattern}")

        # 询问是否匹配完整路径
        full_path_input = input("是否匹配完整路径？([Y]/N): ")
        match_full_path = full_path_input.lower() != 'n'

        recursive_input = input("是否递归遍历子目录？([Y]/N): ")
        recursive = recursive_input.lower() != 'n'

        matching_files = find_files(current_directory, pattern, recursive, match_full_path)

        if matching_files:
            print(f"找到 {len(matching_files)} 个匹配的文件。")
            show_files = input("是否显示文件列表？([Y]/N): ")
            if show_files.lower() != 'n':
                for file in matching_files:
                    print(f"    {file}")
            # 移动到回收站
            confirmation = input("是否将这些文件移动到回收站？(Y/[N]): ")
            if confirmation.lower() == 'y':
                for file in matching_files:
                    try:
                        send2trash.send2trash(file)
                        print(f"已移动文件：{file}")
                    except Exception as e:
                        print(f"移动文件 {file} 时出错：{e}")
                print("操作完成。")
            else:
                print("操作已取消。")
        else:
            print("没有找到匹配的文件。")


if __name__ == "__main__":
    main()