#######################

import json
import os
from urllib import request
import time
import PIL.Image
import send2trash
from colorama import init, Fore

#######################

prompt_text = {
  "1": {
    "inputs": {
      "image": "0C31687D5DEC5F00072CD49B809B3CBF.jpg",
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

#######################

init(autoreset=True)

#######################

endpoint = 8188
height_threshold = 1500
image_files = []
img_dir = None
jpg_size_threshold = 700
last_img_dir = None
last_model_file_path = r"C:\AI\StableDiffusion\Stable Diffusion ComfyUI Aki V1.2\models\upscale_models"
long_image_list = []
model_file_path = r"C:\AI\StableDiffusion\Stable Diffusion ComfyUI Aki V1.2\models\upscale_models"
model_files = []
model_index = None
post_downscale_scale = 1
request_interval = 4
width_threshold = 1500

#######################

def set_model_name(model_index):
    model_path = model_files[model_index]
    model_name = os.path.basename(model_path)
    prompt_text["11"]["inputs"]["model_name"] = model_name
    return model_name

#######################

def get_parameters():
    #-------------------------------------
    # 定义放大模型文件路径（默认值）
    global model_file_path
    global last_model_file_path
    # 是否使用自定义模型路径
    print("-"*50)
    while True:
        custom_model = input(f"当前 ComfyUI 放大模型路径：{model_file_path}\n输入新路径来修改当前路径，或留空以不做修改：")
        if custom_model:
            if not os.path.isdir(custom_model):
                print(Fore.RED + "路径不存在")
            else:
                last_model_file_path = model_file_path
                model_file_path = custom_model
                print(f"已将 ComfyUI 放大模型路径修改为：{model_file_path}")
                break
        else:
            print(f"已使用默认路径：{model_file_path}")
            break
    #-------------------------------------
    # 定义模型文件列表
    global model_files
    print("-"*50)
    while True:
        # 若列表为空，则获取模型列表
        if not model_files:
            for file in os.listdir(model_file_path):
                if file.lower().endswith(('.ckpt', '.safetensors', '.pt', '.bin', '.pth')):
                    model_files.append(os.path.join(model_file_path, file))
        # 若更改过模型路径，则获取模型列表
        if last_model_file_path != model_file_path:
            model_files = []
            for file in os.listdir(model_file_path):
                if file.lower().endswith(('.ckpt', '.safetensors', '.pt', '.bin', '.pth')):
                    model_files.append(os.path.join(model_file_path, file))
        if not model_files:
            print(Fore.RED + "未找到模型文件")
            model_file_path = input("请输入自定义模型路径: ")
        else:
            print(f"找到 {len(model_files)} 个模型文件：")
            for i, file in enumerate(model_files):
                file = os.path.basename(file)
                print(f"    {i}、{file}")
            break
    #-------------------------------------
    # 输入序号选择模型文件
    print("-"*50)
    global model_index
    while True:
        # 模型文件没有被设置过
        if model_index is None:
            model_index = input("请输入要使用的模型文件的序号（默认值：0）：")
            try:
                if not model_index:
                    model_index = 0
                    model_name = set_model_name(model_index)
                    print(f"正在使用第 {model_index} 个模型文件：{model_name}")
                    break
                else:
                    try:
                        model_index = int(model_index)
                    except ValueError:
                        print(Fore.RED + "输入无效，请输入一个整数")
                    model_name = set_model_name(model_index)
                    print(Fore.GREEN + f"正在使用第 {model_index} 个模型文件：{model_name}")
                    break
            except IndexError:
                print(Fore.RED + "输入的序号不在范围内")
        # 模型文件已经被设置过
        else:
            print(f"当前选择：第 {model_index} 个模型文件")
            index_change = input("输入新序号来修改当前值，或者留空来保持不变：")
            if index_change:
                try:
                    model_index = int(index_change)
                    model_name = set_model_name(model_index)
                    print(f"正在使用第 {model_index} 个模型文件：{model_name}")
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
    print("-"*50)
    global img_dir
    global last_img_dir
    while True:
        if img_dir is None:
            img_dir = input("请输入图片目录：")
            last_img_dir = img_dir
            if not os.path.isdir(img_dir):
                print(Fore.RED + "图片目录无效")
                img_dir = None
            else:
                print(f"正在使用：{img_dir}")
                break
        else:
            print(f"正在使用：{img_dir}")
            img_dir_change = input("输入目录来修改当前目录，或留空以保持不变：")
            if img_dir_change:
                if not os.path.isdir(img_dir_change):
                    print(Fore.RED + "图片目录无效")
                else:
                    last_img_dir = img_dir
                    img_dir = img_dir_change
                    print(f"正在使用：{img_dir}")
                    break
            else:
                print("未修改当前目录")
                break
    # -------------------------------------
    # 获取图片阈值
    global width_threshold
    global height_threshold
    global jpg_size_threshold
    print("-"*50)
    print(f"当前图片宽度阈值：{width_threshold}")
    print(f"当前图片高度阈值：{height_threshold}")
    print(f"当前图片大小阈值：{jpg_size_threshold}KB")
    # 获取图片宽度阈值
    while True:
        width_threshold_change = input("请输入图片宽阈值来修改当前值，或留空来保持不变：")
        if width_threshold_change:
            try:
                width_threshold_change = int(width_threshold_change)
                if width_threshold_change < 0:
                    print(Fore.RED + "输入无效，请输入一个大于等于0的整数")
                else:
                    width_threshold = width_threshold_change
                    print(Fore.GREEN + f"宽阈值已设置为 {width_threshold}")
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
                    height_threshold = height_threshold_change
                    print(Fore.GREEN + f"高阈值已设置为 {height_threshold}")
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
                    jpg_size_threshold = jpg_size_threshold_change
                    print(Fore.GREEN + f"大小阈值已设置为 {jpg_size_threshold}KB")
                    break
            except ValueError:
                print(Fore.RED + "输入无效，请输入一个整数")
        else:
            print(Fore.GREEN + "大小阈值保持不变")
            break
    # -------------------------------------
    # 放大后缩小设置
    print("-"*50)
    global post_downscale_scale
    print(f"当前放大后的图片缩小比例：{post_downscale_scale}")
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
                    post_downscale_scale = float(post_downscale_scale_change)
                    print(Fore.GREEN + f"缩小比例已设置为 {post_downscale_scale}")
                    break
            except ValueError:
                print(Fore.RED + "输入无效，请输入一个数字")
        else:
            print("使用默认缩小比例")
            break
    prompt_text["6"]["inputs"]["scale_by"] = post_downscale_scale
    # -------------------------------------
    # 端口
    print("-"*50)
    global endpoint
    print(f"当前端口号：{endpoint}")
    while True:
        endpoint_change = input("请输入端口号来修改当前值，留空使用默认值：")
        if endpoint_change:
            try:
                endpoint = int(endpoint_change)
                print(Fore.GREEN + f"端口号已设置为 {endpoint}")
                break
            except ValueError:
                print(Fore.RED + "输入无效，请输入一个整数")
        else:
            print("使用默认端口号")
            break
    # -------------------------------------
    # 请求间隔
    print("-"*50)
    global request_interval
    print(f"当前请求间隔：{request_interval}")
    while True:
        request_interval_change = input("输入新的请求间隔来修改当前值，或留空以不做修改：")
        if request_interval_change:
            try:
                request_interval_change = float(request_interval_change)
                if request_interval_change <= 0:
                    print(Fore.RED + "输入无效，请输入一个大于0的数字")
                else:
                    request_interval = float(request_interval_change)
                    print(Fore.GREEN + f"请求间隔已设置为 {request_interval}")
                    break
            except ValueError:
                print(Fore.RED + "输入无效，请输入一个数字")
        else:
            print(Fore.GREEN + "请求间隔保持不变")
            break

#######################

# 定义 queue_prompt 函数
def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request(f"http://127.0.0.1:{endpoint}/prompt", data=data)
    request.urlopen(req)
    time.sleep(request_interval)

#######################

def get_image_files():
    global image_files
    global img_dir
    global last_img_dir
    # 如果列表已存在，且图片目录未被更改，则跳过查找
    if image_files and last_img_dir == img_dir:
        print("图片文件列表已存在，跳过查找")
        pass
    else:
        # 检查图片文件是否满足以下要求
        try:
            image_files = []
            # 1、是任意非 gif 图像文件，且长宽有至少一个值小于 1500
            for file in os.listdir(img_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')) and not file.lower().endswith(
                        '.gif'):
                    image_path = os.path.join(img_dir, file)
                    image = PIL.Image.open(image_path)
                    if image.size[0] < width_threshold or image.size[1] < height_threshold:
                        image_files.append(image_path)
            # 2、是 jpg 图像文件，且大小小于 700KB
            for file in os.listdir(img_dir):
                if file.lower().endswith(('.jpg', '.jpeg')):
                    image_path = os.path.join(img_dir, file)
                    if os.path.getsize(image_path) < jpg_size_threshold * 1024:
                        image_files.append(image_path)
        except FileNotFoundError:
            print("图片目录不存在")
        except Exception as e:
            print(f"发生错误：{e}")


        # 去除重复值
        image_files = list(set(image_files))

        # 判断是否是长图
        for image_file in image_files:
            image = PIL.Image.open(image_file)
            # 根据长宽/宽长比例判断
            if image.size[0] / image.size[1] > 2.5 or image.size[1] / image.size[0] > 2.5:
                skip_confirm = input(f"    {image_file} 看起来是长图，要忽略吗([Y]/N): ")
                if skip_confirm.lower() != 'n':
                    image_files.remove(image_file)

        # 转换相对路径为绝对路径
        for i in range(len(image_files)):
            image_files[i] = os.path.abspath(image_files[i])

        # 按文件名字母顺序排序
        image_files.sort(key=lambda x: os.path.basename(x))

        # 检查是否有图片包含透明度
        for image_file in image_files:
            with PIL.Image.open(image_file) as img:
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    image_files.remove(image_file)
                    print(f"    {image_file} 包含透明度，已丢弃。")

        # 打印图片文件列表
        print("找到的图片文件列表：")
        for image_file in image_files:
            print(f"    {image_file}")
        print(f"共找到 {len(image_files)} 张图片。")

#######################

def send_request():
    get_image_files()
    input("按回车键开始发送请求")
    # 遍历图片文件并更新 JSON 中的 "image" 值
    for image_file in image_files:
        prompt_text["1"]["inputs"]["image"] = image_file
        prompt_text["1"]["inputs"]["upload"] = "image"  # 假设这个也应该更新

        # 使用更新后的 JSON 调用 queue_prompt 函数
        queue_prompt(prompt_text)
        print(f"已发送请求：{image_file}")

        # 打印图片分辨率和大小
        current_image = PIL.Image.open(image_file)
        print(f"    图片分辨率：{current_image.size}")
        print(f"    图片大小：{os.path.getsize(image_file) / 1024}KB")

#######################

def send_to_trash():
    # 是否发送原图片文件到回收站
    del_confirm = input("是否将原图片文件发送到回收站？(y/n): ")
    if del_confirm.lower() == 'y':
        for image_file in image_files:
            send2trash.send2trash(image_file)
            print(f"已删除文件：{image_file}")
    else:
        print("原图片文件未删除。")

#######################

def manual():
    # 手动输入图片路径
    image_file = input("请输入图片路径：")
    prompt_text["1"]["inputs"]["image"] = image_file
    prompt_text["1"]["inputs"]["upload"] = "image"  # 假设这个也应该更新

    # 使用更新后的 JSON 调用 queue_prompt 函数
    queue_prompt(prompt_text)
    print(f"已发送请求：{image_file}")

#######################

def main():
    while True:
        print("-"*50)
        choice = input("请选择操作：\n1. 获取参数\n2. 退出\n请输入选项：")
        if choice == '1':
            get_parameters()
            while True:
                print("-"*50)
                choice = input("请选择操作：\n1. 放大图片（自动查找）\n2. 放大图片（手动指定）\n3. 删除图片文件\n4. 重新获取参数\n请输入选项：")
                if choice == '1':
                    send_request()
                elif choice == '2':
                    manual()
                elif choice == '3':
                    send_to_trash()
                elif choice == '4':
                    break
                else:
                    print("无效的选项，请重新输入。")
        elif choice == '2':
            break
        else:
            print("无效的选项，请重新输入。")

#######################

if __name__ == "__main__":
    main()
