import re

import charset_normalizer


def convert_unicode_escape(text):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)

def process_file(input_file, output_file):
    try:
        # 检测文件编码
        with open(input_file, 'rb') as file:
            content_bytes = file.read()

        encoding_info = charset_normalizer.detect(content_bytes)
        print("检测到的编码信息：", encoding_info)
        encoding = encoding_info['encoding'] if encoding_info else 'utf-8'

        with open(input_file, 'r', encoding=encoding) as file:
            content = file.read()

        converted_content = convert_unicode_escape(content)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(converted_content)

        print(f"转换完成，结果已保存到 {output_file}")

    except Exception as e:
        print(f"处理文件时出错: {e}")

if __name__ == "__main__":
    input_file = input("请输入要处理的文件路径: ")
    output_file = input("请输入保存结果的文件路径: ")

    process_file(input_file, output_file)