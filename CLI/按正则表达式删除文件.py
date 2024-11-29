import os
import re
import send2trash


def find_files(directory, regex_pattern):
    pattern = re.compile(regex_pattern)
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern.search(file):
                matching_files.append(os.path.join(root, file))
    return matching_files


def main():
    print("输入'---quit'以停止脚本。")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_directory = script_dir
    current_regex_pattern = ".+"

    while True:
        directory_change = input(f"请输入目录路径 (当前: {current_directory}): ")
        if directory_change == "---quit":
            print("脚本已停止。")
            break
        if directory_change:
            current_directory = directory_change
        else:
            print(f"目录未改变：{current_directory}")

        regex_pattern_change = input(f"请输入正则表达式 (当前: {current_regex_pattern}): ")
        if regex_pattern_change == "---quit":
            print("脚本已停止。")
            break
        if regex_pattern_change:
            current_regex_pattern = regex_pattern_change
        else:
            print(f"正则表达式未改变：{current_regex_pattern}")

        matching_files = find_files(current_directory, current_regex_pattern)

        if matching_files:
            print("找到以下匹配的文件:")
            for file in matching_files:
                print(file)
            confirmation = input("是否将这些文件移动到回收站？(Y/[N]): ")
            if confirmation.lower() == 'y':
                for file in matching_files:
                    send2trash.send2trash(file)
                print("文件已移动到回收站。")
            else:
                print("操作已取消。")
        else:
            print("没有找到匹配的文件。")


if __name__ == "__main__":
    main()
