import json
import random
import pyperclip
import pandas
import os
import charset_normalizer

predefined_path = {
    "KohakuXL Delta": r"C:\AI\StableDiffusion\Dataset\KohakuXL Delta\artists-kxl-delta.json",
    "NoobAI XL Danbooru": r"C:\AI\StableDiffusion\Dataset\NoobXL\danbooru_artist_webui.csv",
    "NoobAI XL e621": r"C:\AI\StableDiffusion\Dataset\NoobXL\e621_artist_webui.csv",
}

# 读取画师文件
current_artists_path = predefined_path["KohakuXL Delta"]
artists_dir_change = input(f"当前画师文件路径：{current_artists_path}，是否要更改？(Y/[N]): ")
if artists_dir_change.lower() == "y":
    while True:
        change_mode = input("1. 自定义路径\n2. 预定义路径\n请选择更改模式：")
        if change_mode == "1":
            artists_path = input("请输入新的画师文件路径：")
            if not os.path.exists(artists_path):
                print("文件不存在，请重新输入")
            else:
                current_artists_path = artists_path
                print(f"画师文件已更新：{current_artists_path}")
                break
        elif change_mode == "2":
            for index, (name, path) in enumerate(predefined_path.items()):
                print(f"{index + 1}. {name}")
            choice = input("请选择预定义路径：")
            if choice.isdigit() and 1 <= int(choice) <= len(predefined_path):
                current_artists_path = predefined_path[list(predefined_path.keys())[int(choice) - 1]]
                print(f"画师文件已更新：{current_artists_path}")
                break
            else:
                print("无效的选择，请重新输入")
        else:
            print("无效的选择，请重新输入")

current_artists_num = 10
artists_num = input("请输入要抽取的画师数量（当前：10）：")
if artists_num:
    current_artists_num = int(artists_num)
    print(f"已更新要抽取的画师数量为：{artists_num}")

# 文件处理逻辑
if current_artists_path.endswith(".json"):  # KXL
    with open(current_artists_path, 'rb') as f:
        content_bytes = f.read()
        encoding = charset_normalizer.detect(content_bytes)
    with open(current_artists_path, 'r', encoding=encoding['encoding']) as f:
        kxl_list = json.load(f)
        artists_list = [item[0] for item in kxl_list]
        weights = [item[1] for item in kxl_list]
elif current_artists_path.endswith(".csv"):  # NAIXL
    with open(current_artists_path, 'rb') as f:
        content_bytes = f.read()
        encoding = charset_normalizer.detect(content_bytes)
    artists_list = pandas.read_csv(current_artists_path, encoding=encoding['encoding'], low_memory=False)[
        'trigger'].tolist()
    weights = pandas.read_csv(current_artists_path, encoding=encoding['encoding'], low_memory=False)['count'].tolist()
else:
    print("不受支持的文件格式")
    exit(1)

chosen_artists_list = random.choices(artists_list, k=current_artists_num, weights=weights)

random_artists_str = ""

# 转字符串逻辑
if current_artists_path.endswith(".json"):  # KXL
    # for artist in chosen_artists_list:
    #     random_artists_str += artist.replace('(', '\\(').replace(')', '\\)') + ", "
    random_artists_str = ", ".join(chosen_artists_list)
    random_artists_str = random_artists_str.replace('(', '\\(').replace(')', '\\)')
else:  # NAIXL
    random_artists_str = ", ".join(chosen_artists_list)

pyperclip.copy(random_artists_str)
print(random_artists_str)