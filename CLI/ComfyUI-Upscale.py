#######################

import json
import os
import time
from urllib import request
from tqdm import tqdm
import PIL.Image
import send2trash
from colorama import init, Fore
import requests

init(autoreset=True)


#######################

class ImageUpscaler:
    def __init__(self):
        self.prompt_text = {
            "1": {
                "inputs": {
                    "image": "example.jpg",
                    "upload": "image"
                },
                "class_type": "LoadImage",
                "_meta": {
                    "title": "加载图像"
                }
            },
            "6": {
                "inputs": {
                    "upscale_method": "lanczos",
                    "scale_by": 0.5,
                    "image": [
                        "10",
                        0
                    ]
                },
                "class_type": "ImageScaleBy",
                "_meta": {
                    "title": "图像按系数缩放"
                }
            },
            "10": {
                "inputs": {
                    "upscale_model": [
                        "11",
                        0
                    ],
                    "image": [
                        "1",
                        0
                    ]
                },
                "class_type": "ImageUpscaleWithModel",
                "_meta": {
                    "title": "图像通过模型放大"
                }
            },
            "11": {
                "inputs": {
                    "model_name": "4x-WTP-UDS-Esrgan.pth"
                },
                "class_type": "UpscaleModelLoader",
                "_meta": {
                    "title": "放大模型加载器"
                }
            },
            "15": {
                "inputs": {
                    "filename_prefix": "Upscale",
                    "images": [
                        "6",
                        0
                    ]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "保存图像"
                }
            }
        }
        self.endpoint = 8188
        self.height_threshold = 1500
        self.image_files = []
        self.img_dir = None
        self.jpg_size_threshold = 700
        self.last_img_dir = None
        self.model_file_path = r"C:\AI\StableDiffusion\Stable Diffusion ComfyUI Aki V1.2\models\upscale_models"
        self.last_model_file_path = r"C:\AI\StableDiffusion\Stable Diffusion ComfyUI Aki V1.2\models\upscale_models"
        self.model_files = []
        self.model_index = None
        self.post_downscale_scale = 1
        self.get_interval = 0.1
        self.width_threshold = 1500
        self.recursive_search = False

    def __getitem__(self, item):
        return self.image_files[item]

    def set_model_name(self, model_index):
        """
        设置放大模型名称
        :param model_index:
        :return:
        """
        model_path = self.model_files[model_index]
        model_name = os.path.basename(model_path)
        self.prompt_text["11"]["inputs"]["model_name"] = model_name
        return model_name

    def get_parameters(self):
        """
        （交互式）获取放大参数
        :return:
        """
        # -------------------------------------
        # 是否使用自定义模型路径
        print("-" * 50)
        while True:
            custom_model = input(
                f"当前 ComfyUI 放大模型路径：{self.model_file_path}\n输入新路径来修改当前路径，或留空以不做修改：")
            if custom_model:
                if not os.path.isdir(custom_model):
                    print(Fore.RED + "路径不存在")
                else:
                    self.last_model_file_path = self.model_file_path
                    model_file_path = custom_model
                    print(f"已将 ComfyUI 放大模型路径修改为：{model_file_path}")
                    break
            else:
                print(f"已使用默认路径：{self.model_file_path}")
                break
        # -------------------------------------
        # 定义模型文件列表
        print("-" * 50)
        while True:
            # 若列表为空，则获取模型列表
            if not self.model_files:
                for file in os.listdir(self.model_file_path):
                    if file.lower().endswith(('.ckpt', '.safetensors', '.pt', '.bin', '.pth')):
                        self.model_files.append(os.path.join(self.model_file_path, file))
            # 若更改过模型路径，则获取模型列表
            if self.last_model_file_path != self.model_file_path:
                self.model_files = []
                for file in os.listdir(self.model_file_path):
                    if file.lower().endswith(('.ckpt', '.safetensors', '.pt', '.bin', '.pth')):
                        self.model_files.append(os.path.join(self.model_file_path, file))
            if not self.model_files:
                print(Fore.RED + "未找到模型文件")
                self.model_file_path = input("请输入自定义模型路径: ")
            else:
                print(f"找到 {len(self.model_files)} 个模型文件：")
                for i, file in enumerate(self.model_files):
                    file = os.path.basename(file)
                    print(f"    {i}、{file}")
                break
        # -------------------------------------
        # 输入序号选择模型文件
        print("-" * 50)
        while True:
            # 模型文件没有被设置过
            if self.model_index is None:
                self.model_index = input("请输入要使用的模型文件的序号（默认值：0）：")
                try:
                    if not self.model_index:
                        self.model_index = 0
                        model_name = self.set_model_name(self.model_index)
                        print(f"正在使用第 {self.model_index} 个模型文件：{model_name}")
                        break
                    else:
                        try:
                            self.model_index = int(self.model_index)
                        except ValueError:
                            print(Fore.RED + "输入无效，请输入一个整数")
                        model_name = self.set_model_name(self.model_index)
                        print(Fore.GREEN + f"正在使用第 {self.model_index} 个模型文件：{model_name}")
                        break
                except IndexError:
                    print(Fore.RED + "输入的序号不在范围内")
            # 模型文件已经被设置过
            else:
                print(f"当前选择：第 {self.model_index} 个模型文件")
                index_change = input("输入新序号来修改当前值，或者留空来保持不变：")
                if index_change:
                    try:
                        self.model_index = int(index_change)
                        model_name = self.set_model_name(self.model_index)
                        print(f"正在使用第 {self.model_index} 个模型文件：{model_name}")
                        break
                    except ValueError:
                        print(Fore.RED + "输入无效，请输入一个整数")
                    except IndexError:
                        print(Fore.RED + "输入的序号不在范围内")
                else:
                    print("未修改当前序号")
                    break
        # -------------------------------------
        # 获取图片目录
        print("-" * 50)
        while True:
            if self.img_dir is None:
                self.img_dir = input("请输入图片目录：")
                self.last_img_dir = self.img_dir
                if not os.path.isdir(self.img_dir):
                    print(Fore.RED + "图片目录无效")
                    self.img_dir = None
                else:
                    print(f"正在使用：{self.img_dir}")
                    break
            else:
                print(f"正在使用：{self.img_dir}")
                img_dir_change = input("输入目录来修改当前目录，或留空以保持不变：")
                if img_dir_change:
                    if not os.path.isdir(img_dir_change):
                        print(Fore.RED + "图片目录无效")
                    else:
                        self.last_img_dir = self.img_dir
                        self.img_dir = img_dir_change
                        print(f"正在使用：{self.img_dir}")
                        break
                else:
                    print("未修改当前目录")
                    break
        # 是否递归查找子目录
        print("-" * 50)
        recursive_search_input = input("是否递归查找子目录中的图片？(Y/[N]): ")
        self.recursive_search = recursive_search_input.lower() == 'y'
        print(f"递归查找设置为：{self.recursive_search}")
        # -------------------------------------
        # 获取图片阈值
        print("-" * 50)
        print(f"当前图片宽度阈值：{self.width_threshold}")
        print(f"当前图片高度阈值：{self.height_threshold}")
        print(f"当前图片大小阈值：{self.jpg_size_threshold}KB")
        # 获取图片宽度阈值
        while True:
            width_threshold_change = input("请输入图片宽阈值来修改当前值，或留空来保持不变：")
            if width_threshold_change:
                try:
                    width_threshold_change = int(width_threshold_change)
                    if width_threshold_change < 0:
                        print(Fore.RED + "输入无效，请输入一个大于等于0的整数")
                    else:
                        self.width_threshold = width_threshold_change
                        print(Fore.GREEN + f"宽阈值已设置为 {self.width_threshold}")
                        break
                except ValueError:
                    print(Fore.RED + "输入无效，请输入一个整数")
            else:
                print(Fore.GREEN + "宽阈值保持不变")
                break
        # 获取图片高度阈值
        while True:
            height_threshold_change = input("请输入图片高阈值来修改当前值，或留空来保持不变：")
            if height_threshold_change:
                try:
                    height_threshold_change = int(height_threshold_change)
                    if height_threshold_change < 0:
                        print(Fore.RED + "输入无效，请输入一个大于等于0的整数")
                    else:
                        self.height_threshold = height_threshold_change
                        print(Fore.GREEN + f"高阈值已设置为 {self.height_threshold}")
                        break
                except ValueError:
                    print(Fore.RED + "输入无效，请输入一个整数")
            else:
                print(Fore.GREEN + "高阈值保持不变")
                break
        # 获取 jpg 大小阈值
        while True:
            jpg_size_threshold_change = input("请输入图片大小阈值来修改当前值，或留空来保持不变：")
            if jpg_size_threshold_change:
                try:
                    jpg_size_threshold_change = int(jpg_size_threshold_change)
                    if jpg_size_threshold_change < 0:
                        print(Fore.RED + "输入无效，请输入一个大于等于0的整数")
                    else:
                        self.jpg_size_threshold = jpg_size_threshold_change
                        print(Fore.GREEN + f"大小阈值已设置为 {self.jpg_size_threshold}KB")
                        break
                except ValueError:
                    print(Fore.RED + "输入无效，请输入一个整数")
            else:
                print(Fore.GREEN + "大小阈值保持不变")
                break
        # -------------------------------------
        # 放大后缩小设置
        print("-" * 50)
        print(f"当前放大后的图片缩小比例：{self.post_downscale_scale}")
        while True:
            post_downscale_scale_change = input("输入比例来更改当前值，留空使用默认值：")
            if post_downscale_scale_change:
                try:
                    post_downscale_scale_change = float(post_downscale_scale_change)
                    if post_downscale_scale_change <= 0:
                        print(Fore.RED + "输入无效，请输入一个大于0的数字")
                    elif post_downscale_scale_change > 1:
                        print(Fore.RED + "输入无效，请输入一个小于等于1的数字")
                    else:
                        self.post_downscale_scale = float(post_downscale_scale_change)
                        print(Fore.GREEN + f"缩小比例已设置为 {self.post_downscale_scale}")
                        break
                except ValueError:
                    print(Fore.RED + "输入无效，请输入一个数字")
            else:
                print("使用默认缩小比例")
                break
        self.prompt_text["6"]["inputs"]["scale_by"] = self.post_downscale_scale
        # -------------------------------------
        # 端口
        print("-" * 50)
        print(f"当前端口号：{self.endpoint}")
        while True:
            endpoint_change = input("请输入端口号来修改当前值，留空使用默认值：")
            if endpoint_change:
                try:
                    self.endpoint = int(endpoint_change)
                    print(Fore.GREEN + f"端口号已设置为 {self.endpoint}")
                    break
                except ValueError:
                    print(Fore.RED + "输入无效，请输入一个整数")
            else:
                print("使用默认端口号")
                break
        # -------------------------------------
        # 请求间隔
        print("-" * 50)
        print(f"当前查询间隔（每隔这段时间，脚本都会查询上次的任务是否已经完成）：{self.get_interval}")
        while True:
            request_interval_change = input("输入新的查询间隔来修改当前值，或留空以不做修改：")
            if request_interval_change:
                try:
                    request_interval_change = float(request_interval_change)
                    if request_interval_change <= 0:
                        print(Fore.RED + "输入无效，请输入一个大于0的数字")
                    else:
                        self.get_interval = float(request_interval_change)
                        print(Fore.GREEN + f"请求间隔已设置为 {self.get_interval}")
                        break
                except ValueError:
                    print(Fore.RED + "输入无效，请输入一个数字")
            else:
                print(Fore.GREEN + "请求间隔保持不变")
                break

    def get_image_files(self):
        """
        获取图片文件列表
        :return:
        """
        # 如果列表已存在，且图片目录未被更改，则跳过查找
        if self.image_files and self.last_img_dir == self.img_dir:
            print("图片文件列表已存在，跳过查找")
            pass
        else:
            self.image_files = []
            if self.recursive_search:
                # 递归查找
                for root, dirs, files in os.walk(self.img_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # 检查文件是否符合图片文件的要求
                        # 1、是任意非 gif 图像文件，且长宽有至少一个值小于 1500
                        if file_path.lower().endswith(
                                ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')) and not file_path.lower().endswith(
                                '.gif'):
                            try:
                                image = PIL.Image.open(file_path)
                                if image.size[0] < self.width_threshold or image.size[1] < self.height_threshold:
                                    self.image_files.append(file_path)
                            except Exception as e:
                                print(f"无法打开文件 {file_path}: {e}")
                        # 2、是 jpg 图像文件，且大小小于 700KB
                        if file_path.lower().endswith(('.jpg', '.jpeg')) and os.path.getsize(
                                file_path) < self.jpg_size_threshold * 1024:
                            self.image_files.append(file_path)
            else:
                # 非递归查找
                for file in os.listdir(self.img_dir):
                    file_path = os.path.join(self.img_dir, file)
                    if os.path.isfile(file_path):
                        # 检查文件是否符合图片文件的要求
                        # 1、是任意非 gif 图像文件，且长宽有至少一个值小于 1500
                        if file_path.lower().endswith(
                                ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')) and not file_path.lower().endswith(
                                '.gif'):
                            try:
                                image = PIL.Image.open(file_path)
                                if image.size[0] < self.width_threshold or image.size[1] < self.height_threshold:
                                    self.image_files.append(file_path)
                            except Exception as e:
                                print(f"无法打开文件 {file_path}: {e}")
                        # 2、是 jpg 图像文件，且大小小于 700KB
                        if file_path.lower().endswith(('.jpg', '.jpeg')) and os.path.getsize(
                                file_path) < self.jpg_size_threshold * 1024:
                            self.image_files.append(file_path)
            # 去除重复值
            self.image_files = list(set(self.image_files))
            # 判断是否是长图
            for image_file in self.image_files:
                image = PIL.Image.open(image_file)
                if image.size[0] / image.size[1] > 2.5 or image.size[1] / image.size[0] > 2.5:
                    skip_confirm = input(f"    {image_file} 看起来是长图，要忽略吗([Y]/N): ")
                    if skip_confirm.lower() != 'n':
                        self.image_files.remove(image_file)
            # 转换相对路径为绝对路径
            for i in range(len(self.image_files)):
                self.image_files[i] = os.path.abspath(self.image_files[i])
            # 排序
            self.image_files.sort(key=lambda x: os.path.basename(x))
            # 检查是否有图片包含透明度
            for image_file in self.image_files:
                with PIL.Image.open(image_file) as img:
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        self.image_files.remove(image_file)
                        print(f"    {image_file} 包含透明度，已丢弃。")

            print("找到的图片文件列表：")
            for image_file in self.image_files:
                print(f"    {image_file}")
            print(f"共找到 {len(self.image_files)} 张图片。")

    def send_request(self):
        self.get_image_files()
        input("按回车键开始发送请求")
        # 遍历图片文件并更新 JSON 中的 "image" 值
        for image_file in tqdm(self.image_files):
            self.prompt_text["1"]["inputs"]["image"] = image_file
            self.prompt_text["1"]["inputs"]["upload"] = "image"
            self.prompt_text["15"]["inputs"]["filename_prefix"] = os.path.splitext(os.path.basename(image_file))[0]
            # 使用更新后的 JSON 调用 queue_prompt 函数
            self.queue_prompt(self.prompt_text)
            tqdm.write(f"已发送请求：{image_file}")
            # 打印图片分辨率和大小
            current_image = PIL.Image.open(image_file)
            tqdm.write(f"    图片分辨率：{current_image.size}")
            tqdm.write(f"    图片大小：{os.path.getsize(image_file) / 1024}KB")

    def queue_prompt(self, prompt):
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')
        req = request.Request(f"http://127.0.0.1:{self.endpoint}/prompt", data=data)
        request.urlopen(req)
        while True:
            time.sleep(self.get_interval)
            remaining_queue = requests.get(f"http://127.0.0.1:{self.endpoint}/prompt").json()
            remaining_queue = remaining_queue["exec_info"]["queue_remaining"]
            if remaining_queue == 0:
                break

    def send_to_trash(self):
        del_confirm = input("是否将原图片文件发送到回收站？(Y/[N]): ")
        if del_confirm.lower() == 'y':
            for image_file in tqdm(self.image_files):
                send2trash.send2trash(image_file)
                tqdm.write(f"已删除文件：{image_file}")
        else:
            print("原图片文件未删除。")

    def manual(self):
        manual_file = input("请输入图片路径或包含图片路径的txt文件：")
        if os.path.isfile(manual_file):
            # 是图片
            if manual_file.lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')) and not manual_file.lower().endswith('.gif'):
                self.prompt_text["1"]["inputs"]["image"] = manual_file
                self.prompt_text["1"]["inputs"]["upload"] = "image"
                self.prompt_text["15"]["inputs"]["filename_prefix"] = os.path.splitext(os.path.basename(manual_file))[0]
                self.queue_prompt(self.prompt_text)
                print(f"已发送请求：{manual_file}")
            # 是文本文件
            elif manual_file.lower().endswith('.txt'):
                self.image_files = []
                with open(manual_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                image_files = [line.strip() for line in lines if line.strip().lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')) and not line.strip().lower().endswith('.gif')]
                for image_file in tqdm(image_files):
                    self.prompt_text["1"]["inputs"]["image"] = image_file
                    self.prompt_text["1"]["inputs"]["upload"] = "image"
                    self.prompt_text["15"]["inputs"]["filename_prefix"] = \
                    os.path.splitext(os.path.basename(image_file))[0]
                    self.queue_prompt(self.prompt_text)
                    tqdm.write(f"已发送请求：{image_file}")
                    while True:
                        time.sleep(self.get_interval)
                        remaining_queue = requests.get(f"http://127.0.0.1:{self.endpoint}/prompt").json()
                        remaining_queue = remaining_queue["exec_info"]["queue_remaining"]
                        if remaining_queue == 0:
                            break
            else:
                print("无效的文件路径或文件类型。")
        else:
            print("文件路径无效")

    def main(self):
        while True:
            print("-" * 50)
            choice = input("请选择操作：\n1. 获取参数\n2. 退出\n请输入选项：")
            if choice == '1':
                self.get_parameters()
                while True:
                    print("-" * 50)
                    choice = input(
                        "请选择操作：\n1. 放大图片（自动查找）\n2. 放大图片（手动指定）\n3. 删除图片文件\n4. 重新获取参数\n请输入选项：")
                    if choice == '1':
                        self.send_request()
                    elif choice == '2':
                        self.manual()
                    elif choice == '3':
                        self.send_to_trash()
                    elif choice == '4':
                        break
                    else:
                        print("无效的选项，请重新输入。")
            elif choice == '2':
                break
            else:
                print("无效的选项，请重新输入。.")


#######################

if __name__ == "__main__":
    upscaler = ImageUpscaler()
    upscaler.main()
