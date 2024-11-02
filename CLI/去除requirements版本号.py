import re
from idlelib.iomenu import encoding


def remove_versions_from_requirements(file_path):
    # 正则表达式匹配包名及其后面的版本号
    pattern = re.compile(r"(\S+)==[\d\w\.]+")

    # 检查文件编码
    encoding = input("请输入文件编码（如utf-8）：")

    try:
        with open(file_path, 'r', encoding=encoding) as file:
            lines = file.readlines()

        # 移除版本号
        no_version_lines = [pattern.sub(r'\1', line).strip() for line in lines]

        # 保存到新文件
        with open('requirements-noversion.txt', 'w', encoding="utf-8") as new_file:
            for line in no_version_lines:
                new_file.write(line + '\n')

        print(f"版本号已移除，结果已保存到 'requirements-noversion.txt'")

    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
    except Exception as e:
        print(f"发生错误：{e}")

# 用户输入文件路径
input_path = input("请输入requirements.txt文件的路径：")
remove_versions_from_requirements(input_path)
