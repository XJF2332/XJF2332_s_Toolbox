import os
import re
import shutil

search_dir = os.path.dirname(os.path.abspath(__file__))
destination_dir = os.path.join(search_dir, "Copied_Folders")
regex_pattern = ".*"
whitelist = set()  # 白名单集合

search_dir_change = input(f"请输入要搜索的文件夹路径（当前：{search_dir}）")
if search_dir_change:
    search_dir = search_dir_change
    print(f"搜索文件夹路径已更改为：{search_dir}")
destination_dir_change = input(f"请输入要复制到的目标文件夹路径（当前：{destination_dir}）")
if destination_dir_change:
    destination_dir = destination_dir_change
    print(f"目标文件夹路径已更改为：{destination_dir}")
regex_pattern_change = input(f"请输入要匹配的目录名称的正则表达式（当前：{regex_pattern}）")
if regex_pattern_change:
    regex_pattern = regex_pattern_change
    print(f"正则表达式已更改为：{regex_pattern}")

# 确保目标文件夹存在
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# 遍历目录
for root, dirs, files in os.walk(search_dir):
    for dir_name in dirs:
        # 检查目录名称是否符合正则表达式
        if re.match(regex_pattern, dir_name):
            # 构建源目录和目标目录的完整路径
            src_dir = os.path.join(root, dir_name)
            dest_dir = os.path.join(destination_dir, dir_name)

            # 如果目录已在白名单中，则跳过
            if src_dir in whitelist:
                continue

            # 复制目录
            try:
                shutil.copytree(src_dir, dest_dir)
                print(f"已将 {src_dir} 复制到 {dest_dir}")
            except FileExistsError:
                print(f"目标目录 {dest_dir} 已存在，跳过复制")

            # 将复制的目录添加到白名单
            whitelist.add(src_dir)

            # 将子目录添加到白名单
            for sub_dir in os.listdir(src_dir):
                sub_dir_path = os.path.join(src_dir, sub_dir)
                if os.path.isdir(sub_dir_path):
                    whitelist.add(sub_dir_path)

    # 检查目录中的文件是否有符合表达式的
    for file_name in files:
        if re.match(regex_pattern, file_name):
            # 构建源文件和目标文件的完整路径
            src_file = os.path.join(root, file_name)
            dest_file = os.path.join(destination_dir, file_name)
            shutil.copy2(src_file, dest_file)
            print(f"已将 {src_file} 复制到 {dest_file}")

