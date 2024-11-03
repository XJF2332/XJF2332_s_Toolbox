import os
import re
import send2trash
import threading

def move_files_to_trash(files):
    for file in files:
        send2trash.send2trash(file)
    print(f"已将以下文件移动到回收站: {files}")

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
    thread_pool = []

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

        matching_files = find_files(current_directory, regex_pattern_change)

        if matching_files:
            print("找到以下匹配的文件:")
            for file in matching_files:
                print(file)
            confirmation = input("是否将这些文件移动到回收站？(Y/[N]): ")
            if confirmation.lower() == 'y':
                # 分组文件并创建线程
                num_threads = 4  # 可以根据需要调整线程数
                files_per_thread = len(matching_files) // num_threads
                for i in range(num_threads):
                    start_index = i * files_per_thread
                    end_index = (i + 1) * files_per_thread if i != num_threads - 1 else len(matching_files)
                    files_to_move = matching_files[start_index:end_index]
                    thread = threading.Thread(target=move_files_to_trash, args=(files_to_move,))
                    thread_pool.append(thread)
                    thread.start()

                # 等待所有线程完成
                for thread in thread_pool:
                    thread.join()
                print("文件已移动到回收站。")
            else:
                print("操作已取消。")
        else:
            print("没有找到匹配的文件。")

if __name__ == "__main__":
    main()
