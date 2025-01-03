import os
import charset_normalizer
import re
import subprocess
from colorama import Fore, init

init(autoreset=True)


def get_valid_int_input(prompt, valid_values):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_values:
                return value
            else:
                print(Fore.RED + f"无效的输入，请输入{valid_values}")
        except ValueError:
            print(Fore.RED + "无效的输入，请输入数字")


def get_yes_no_input(prompt, default='y'):
    while True:
        response = input(prompt).strip().lower()
        if response == '' and default is not None:
            return default
        if response in ['y', 'n']:
            return response
        else:
            print(Fore.RED + "无效的输入，请输入Y或N")


def get_replace_input(prompt, paths, line):
    while True:
        replace_input = input(prompt)
        if replace_input == "---del":
            print(Fore.LIGHTYELLOW_EX + f"removed: {line}")
            return None
        elif replace_input == "---pass":
            print(Fore.LIGHTYELLOW_EX + f"passed: {line}")
            return line
        elif os.path.isfile(replace_input) or os.path.isdir(replace_input):
            return replace_input
        else:
            try:
                replace_index = int(replace_input)
                if 0 <= replace_index < len(paths):
                    replacement = paths[replace_index]
                    print(Fore.LIGHTYELLOW_EX + f"replaced: {line} -> {replacement}")
                    return replacement
                else:
                    print(Fore.RED + f"无效的索引，请输入0到{len(paths) - 1}之间的数字，或者输入特殊命令")
            except ValueError:
                print(Fore.RED + "无效的输入，请输入索引数字或特殊命令")


path = input("请输入包含路径的文本路径：")
method = get_valid_int_input(
    """请输入无效路径的处理方法（1.删除/2.替换）：
    即使是在替换模式下，你也可以输入“---del”来删除
    在替换模式下，你也可以输入“---pass”来跳过当前项
    在替换模式下，如果Everything没找到你想要的文件，你可以直接输入路径来手动指定
    当然，手动模式下，前两个命令也能使用：""", [1, 2])

use_everything_flag = get_yes_no_input("是否使用 Everything 搜索（[Y]/N）：", default='y')
use_everything = True if use_everything_flag == 'y' else False

white_list = [
    r"#EXTM3U"
]
white_list_regex = [
    r"#.+\.m3u8",
    r"#.+"
]

with open(path, 'rb') as data:
    content_bytes = data.read()

encoding = charset_normalizer.detect(content_bytes)['encoding']

with open(path, 'r', encoding=encoding) as file:
    lines = file.readlines()

with open(path, 'w', encoding=encoding) as f:
    seen = []
    for line in lines:
        line = line.replace("\n", "")
        # 白名单
        if line in white_list:
            print(f"white_list: {line}")
            seen.append(line + "\n")
        # 白名单正则
        elif any(re.match(regex, line) for regex in white_list_regex):
            print(f"white_list_regex: {line}")
            seen.append(line + "\n")
        # 无效路径
        elif not os.path.isfile(line) and not os.path.isdir(line):
            # 移除
            if method == 1:
                print(f"removed: {line}")
                continue
            # 替换
            elif method == 2:
                # 使用everything
                if use_everything:
                    query = os.path.splitext(os.path.basename(line))[0]
                    result = subprocess.run(["es", "-s", "-regex", f".*{query}"], capture_output=True, text=True)
                    # 搜索成功
                    if result.returncode == 0:
                        paths = result.stdout.splitlines()
                        if paths:
                            for index, path in enumerate(paths):
                                print(f"{index}: {path}")
                            prompt = f"请输入替换 {line} 的内容："
                            replacement = get_replace_input(prompt, paths, line)
                            if replacement is not None:
                                seen.append(replacement + "\n")
                        else:
                            print(f"未找到 {line} 的替换内容")
                            replacement = get_replace_input(f"请输入替换 {line} 的内容：", [], line)
                            if replacement is not None:
                                seen.append(replacement + "\n")
                    else:
                        print(f"未找到 {line} 的替换内容")
                        replacement = get_replace_input(f"请输入替换 {line} 的内容：", [], line)
                        if replacement is not None:
                            seen.append(replacement + "\n")
                # 不使用everything
                else:
                    replacement = get_replace_input(f"请输入替换 {line} 的内容：", [], line)
                    if replacement is not None:
                        seen.append(replacement + "\n")
        # 有效路径
        else:
            seen.append(line + "\n")

    print("正在写入文件")
    f.writelines(seen)

input("任务完成")
