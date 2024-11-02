# 字符串按字母顺序排序，若出现中文，则按照拼音字母顺序排序。
import pypinyin
import re

# 创建空列表储存用户输入
input_list = []

# 用户输入字符串，"|"分割，"#quit"退出
while True:
    input_str = input("请输入一个字符串，以|分割，输入#quit退出：")
    if input_str == "#quit":
        break
    input_list = input_str.split("|")

# 用正则表达式实现排序函数
def sort_strings(str_list):
    # 去除字符串中的空格
    str_list = [re.sub('\s+', '', s) for s in str_list]
    # 提取中文部分，并按照拼音字母顺序排序
    pinyin_list = [''.join(pypinyin.lazy_pinyin(s)) for s in str_list]
    pinyin_list.sort()
    # 提取中文部分，并按照拼音字母顺序排序
    sorted_list = [re.sub('[^a-zA-Z]', '',
                               pinyin) for pinyin in pinyin_list]
    # 提取英文部分，并按照字母顺序排序
    sorted_list = [re.sub('[^a-zA-Z]', '', s) for s in sorted_list]
    sorted_list.sort()

    # 合并中英文部分
    final_list = [sorted_list[i] + sorted_list[i + 1] for i in range(0, len(sorted_list), 2)]

    return final_list

# 调用排序函数
input_list = sort_strings(input_list)

# 输出排序后的字符串列表
print(input_list)