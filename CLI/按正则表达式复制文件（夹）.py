import os
import re
import shutil

def copy_item(src, dest, whitelist, is_dir):
    if src in whitelist:
        print(f"{src} 已在白名单中，跳过复制")
        return
    if is_dir:
        try:
            shutil.copytree(src, dest)
            print(f"已将 {src} 复制到 {dest}")
            whitelist.add(src)
        except FileExistsError:
            print(f"目标目录 {dest} 已存在，跳过复制")
    else:
        shutil.copy2(src, dest)
        print(f"已将 {src} 复制到 {dest}")

def main():
    search_dir = os.path.dirname(os.path.abspath(__file__))
    destination_dir = os.path.join(search_dir, "Copied_Folders")
    regex_pattern = ".*"
    whitelist = set()

    search_dir_change = input(f"请输入要搜索的文件夹路径（当前：{search_dir}）")
    if search_dir_change:
        search_dir = search_dir_change
        print(f"搜索文件夹路径已更改为：{search_dir}")

    destination_dir_change = input(f"请输入要复制到的目标文件夹路径（当前：{destination_dir}）")
    if destination_dir_change:
        destination_dir = destination_dir_change
        print(f"目标文件夹路径已更改为：{destination_dir}")

    regex_pattern_change = input(f"请输入要匹配的目录/文件名称的正则表达式（当前：{regex_pattern}）")
    if regex_pattern_change:
        regex_pattern = regex_pattern_change
        print(f"正则表达式已更改为：{regex_pattern}")

    recursive_input = input("是否递归查找？(Y/N，默认N): ") or "N"
    recursive = recursive_input.upper() == "Y"

    match_dirs_input = input("是否匹配目录？(Y/N，默认Y): ") or "Y"
    match_dirs = match_dirs_input.upper() == "Y"

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    if recursive:
        for root, dirs, files in os.walk(search_dir):
            if match_dirs:
                for dir_name in dirs:
                    if re.fullmatch(regex_pattern, dir_name):
                        src_dir = os.path.join(root, dir_name)
                        relative_path = os.path.relpath(src_dir, search_dir)
                        dest_dir = os.path.join(destination_dir, relative_path)
                        os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
                        copy_item(src_dir, dest_dir, whitelist, True)
            for file_name in files:
                if re.fullmatch(regex_pattern, file_name):
                    src_file = os.path.join(root, file_name)
                    relative_path = os.path.relpath(src_file, search_dir)
                    dest_file = os.path.join(destination_dir, relative_path)
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                    copy_item(src_file, dest_file, whitelist, False)
    else:
        for entry in os.listdir(search_dir):
            entry_path = os.path.join(search_dir, entry)
            dest_path = os.path.join(destination_dir, entry)
            if os.path.isdir(entry_path):
                if match_dirs and re.fullmatch(regex_pattern, entry):
                    copy_item(entry_path, dest_path, whitelist, True)
            elif os.path.isfile(entry_path):
                if re.fullmatch(regex_pattern, entry):
                    copy_item(entry_path, dest_path, whitelist, False)

if __name__ == "__main__":
    main()