import os

def remove_duplicate_lines(input_file_path):
    try:
        seen_lines = []
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line not in seen_lines:
                    seen_lines.append(line)

        output_file_path = os.path.join(os.path.dirname(input_file_path), f"{os.path.splitext(os.path.basename(input_file_path))[0]}_no_duplicates.txt")

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(seen_lines)

        return "处理完成，重复行已删除。"
    except Exception as e:
        return f"发生错误：{str(e)}"

if __name__ == "__main__":
    input_file_path = input("请输入文件路径：")
    result = remove_duplicate_lines(input_file_path)
    print(result)
