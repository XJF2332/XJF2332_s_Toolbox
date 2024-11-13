import json
import random
import pyperclip

current_artists_dir = r"C:\AI\StableDiffusion\Dataset\KohakuXL Delta\artists-kxl-delta.json"
artists_dir = input(f"请输入画师 JSON 文件路径（当前：{current_artists_dir}）：")
if artists_dir:
    current_artists_dir = artists_dir
    print(f"已更新画师 JSON 文件路径为：{current_artists_dir}")

with open(current_artists_dir, 'r', encoding='utf-8') as f:
    artists_list = json.load(f)
    print(f"已加载 {len(artists_list)} 位画师")

current_artists_num = 10
artists_num = input("请输入要抽取的画师数量（当前：10）：")
if artists_num:
    current_artists_num = int(artists_num)
    print(f"已更新要抽取的画师数量为：{artists_num}")

chosen_artists_list = []

for i in range(current_artists_num):
    random_artists = random.choice(artists_list)
    # 在括号()前加转义
    artist_name = random_artists[0].replace('(', '\\(').replace(')', '\\)')
    chosen_artists_list.append(artist_name)

random_artists_str = ""

for artist in chosen_artists_list:
    random_artists_str += artist + ", "

pyperclip.copy(random_artists_str)
print(random_artists_str)