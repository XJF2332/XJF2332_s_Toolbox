import os
import re

import charset_normalizer


def remove_versions_from_requirements(file_path):
    # 正则表达式匹配包名及其后面的版本号
    pattern = re.compile(r"(\S+)==[\d\w\.]+")

    # 检查文件编码
    with open(file_path, 'rb') as file:
        content_bytes = file.read()

    encoding_info = charset_normalizer.detect(content_bytes)
    print("检测到的编码信息：", encoding_info)
    encoding = encoding_info['encoding'] if encoding_info else 'utf-8'

    folder_path = os.path.dirname(file_path)

    try:
        with open(file_path, 'r', encoding=encoding) as file:
            lines = file.readlines()

        no_version_lines = [pattern.sub(r'\1', line).strip() for line in lines]

        with open(os.path.join(folder_path, 'requirements-noversion.txt'), 'w', encoding="utf-8") as new_file:
            for line in no_version_lines:
                new_file.write(line + '\n')

        print(f"版本号已移除，结果已保存到 'requirements-noversion.txt'")

    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
    except Exception as e:
        print(f"发生错误：{e}")

input_path = input("请输入requirements.txt文件的路径：")
remove_versions_from_requirements(input_path)
