import re
import charset_normalizer

# 更新正则表达式以匹配更广泛的Unicode转义
pattern = r'(?:\\u([0-9a-fA-F]{4})|\\U([0-9a-fA-F]{8}))'


def convert_unicode_escape(text):
    """
    将文本中的Unicode转义序列转换为对应的字符。
    支持\\uXXXX和\\UXXXXXXXX形式。
    """

    def replacer(match):
        if match.group(1):
            return chr(int(match.group(1), 16))
        elif match.group(2):
            return chr(int(match.group(2), 16))

    return re.sub(pattern, replacer, text)


def process_file(input_file, output_file):
    """
    处理输入文件，将其中的Unicode转义序列转换为字符，并保存到输出文件。
    """
    try:
        # 检测文件编码
        with open(input_file, 'rb') as file:
            content_bytes = file.read()

        encoding_info = charset_normalizer.detect(content_bytes)
        print("检测到的编码信息：", encoding_info)
        encoding = encoding_info.get('encoding', 'utf-8')

        # 尝试使用检测到的编码读取文件，如果失败则尝试备用编码
        for enc in [encoding, 'GBK', 'ISO-8859-1']:
            try:
                with open(input_file, 'r', encoding=enc) as file:
                    content = file.read()
                break
            except UnicodeDecodeError:
                print(f"使用编码{enc}读取文件失败，尝试备用编码。")
        else:
            print("无法解码文件，使用utf-8进行解码。")
            with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
                content = file.read()

        converted_content = convert_unicode_escape(content)

        # 写入输出文件，使用utf-8编码
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(converted_content)

        print(f"转换完成，结果已保存到 {output_file}")

    except FileNotFoundError:
        print(f"文件未找到：{input_file}")
    except PermissionError:
        print(f"没有权限读取文件：{input_file} 或写入文件：{output_file}")
    except re.error as e:
        print(f"正则表达式错误：{e}")
    except Exception as e:
        print(f"处理文件时出错: {e}")


if __name__ == "__main__":
    input_file = input("请输入要处理的文件路径: ")
    output_file = input("请输入保存结果的文件路径: ")
    pattern_input = input(f"当前匹配模式为“{pattern}”，输入新的模式来修改，或留空保持原样: ")
    if pattern_input:
        try:
            pattern = pattern_input
            re.compile(pattern)  # 验证正则表达式是否有效
        except re.error as e:
            print(f"正则表达式无效：{e}")
            exit(1)

    process_file(input_file, output_file)