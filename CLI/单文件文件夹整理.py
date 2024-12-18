import os
import send2trash
import shutil

def get_folder_path():
    folder_path = input("请输入要处理的文件夹路径：")
    if not os.path.isdir(folder_path):
        print("无效的文件夹路径，请重新输入。")
        return get_folder_path()
    return folder_path

def is_single_file_folder(folder):
    items = os.listdir(folder)
    files = [item for item in items if os.path.isfile(os.path.join(folder, item))]
    subfolders = [item for item in items if os.path.isdir(os.path.join(folder, item))]
    return len(files) == 1 and len(subfolders) == 0

def rename_with_suffix_if_exists(target_path, base_name, extension):
    if not os.path.exists(target_path):
        return target_path
    count = 1
    while True:
        new_name = f"{base_name}_{count}{extension}"
        candidate_path = os.path.join(os.path.dirname(target_path), new_name)
        if not os.path.exists(candidate_path):
            return candidate_path
        count += 1

def process_folder(folder_path):
    if is_single_file_folder(folder_path):
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        file_to_move = files[0]
        parent_folder = os.path.dirname(folder_path)
        new_file_name = os.path.basename(folder_path)
        file_extension = os.path.splitext(file_to_move)[1]
        new_file_path = os.path.join(parent_folder, new_file_name + file_extension)
        if os.path.exists(new_file_path):
            base_name = new_file_name
            extension = file_extension
            new_file_path = rename_with_suffix_if_exists(new_file_path, base_name, extension)
        shutil.move(os.path.join(folder_path, file_to_move), new_file_path)
        send2trash.send2trash(folder_path)
        print(f"已移动文件 '{file_to_move}' 到父文件夹并重命名为 '{os.path.basename(new_file_path)}'，删除文件夹 '{folder_path}'。")
    else:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                process_folder(item_path)
        if is_single_file_folder(folder_path):
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            file_to_move = files[0]
            parent_folder = os.path.dirname(folder_path)
            new_file_name = os.path.basename(folder_path)
            file_extension = os.path.splitext(file_to_move)[1]
            new_file_path = os.path.join(parent_folder, new_file_name + file_extension)
            if os.path.exists(new_file_path):
                base_name = new_file_name
                extension = file_extension
                new_file_path = rename_with_suffix_if_exists(new_file_path, base_name, extension)
            shutil.move(os.path.join(folder_path, file_to_move), new_file_path)
            send2trash.send2trash(folder_path)
            print(f"已移动文件 '{file_to_move}' 到父文件夹并重命名为 '{os.path.basename(new_file_path)}'，删除文件夹 '{folder_path}'。")

def main():
    folder_path = get_folder_path()
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            process_folder(dir_path)

if __name__ == "__main__":
    main()
    input("按回车键退出。")