import base64
import tkinter as tk
from tkinter import messagebox

# 创建编码函数
def encode():
    input_data = input_text.get("1.0", "end-1c")
    encoded_data = base64.b64encode(input_data.encode()).decode()
    output_text.delete("1.0", "end")
    output_text.insert("1.0", encoded_data)

# 创建解码函数，此时，若输出框有内容，则用输出框的内容作为输入，否则用输入框作为输入
def decode():
    input_data = input_text.get("1.0", "end-1c")
    if output_text.get("1.0", "end-1c") != "":
        input_data = output_text.get("1.0", "end-1c")
    decoded_data = base64.b64decode(input_data.encode()).decode()
    # 解码完成后，若输出框内有内容，则解码结果输出到输入框，若输出框内没内容，则输出到输出框
    if output_text.get("1.0", "end-1c") != "":
        input_text.delete("1.0", "end")
        input_text.insert("1.0", decoded_data)

    else:
        output_text.delete("1.0", "end")
        output_text.insert("1.0", decoded_data)

# 创建主窗口，不允许调整大小
root = tk.Tk()
root.resizable(False, False)

# 创建窗口标题
root.title("Base64编解码器")

# 创建输入框，并在上方显示“输入”
input_label = tk.Label(root, text="输入")
input_label.pack()
input_text = tk.Text(root, height=10, width=50)
input_text.pack()

# 创建一定的间隔距离
space_label = tk.Label(root, text="")
space_label.pack()

# 创建输出框，并在上方显示“输出”
output_label = tk.Label(root, text="输出")
output_label.pack()
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

# 创建一定的间隔距离
space_label = tk.Label(root, text="")
space_label.pack()

# 创建编码按钮，并在同一行隔开一定距离创建解码按钮
encode_button = tk.Button(root, text="编码", command=encode)
encode_button.pack(side=tk.LEFT)
decode_button = tk.Button(root, text="解码", command=decode)
decode_button.pack(side=tk.LEFT)

# 创建再次编码和再次解码按钮
# 再次编码函数
def again_encode():
    # 若输出框有内容，则输出框的内容作为输入，否则用输入框作为输入
    if output_text.get("1.0", "end-1c") != "":
        input_data = output_text.get("1.0", "end-1c")
        encoded_data = base64.b64encode(input_data.encode()).decode()
        output_text.delete("1.0", "end")
        output_text.insert("1.0", encoded_data)

    else:
        input_data = input_text.get("1.0", "end-1c")
        encoded_data = base64.b64encode(input_data.encode()).decode()
        output_text.delete("1.0", "end")
        output_text.insert("1.0", encoded_data)
# 再次编码按钮
again_encode_button = tk.Button(root, text="再次编码", command=again_encode)
again_encode_button.pack(side=tk.LEFT)

# 再次解码函数
def again_decode():
    # 始终用输出框作为输入
    input_data = output_text.get("1.0", "end-1c")
    decoded_data = base64.b64decode(input_data.encode()).decode()
    # 解码完成后，结果同步输出到输出框和输入框
    output_text.delete("1.0", "end")
    output_text.insert("1.0", decoded_data)

    if output_text.get("1.0", "end-1c") != "":
        input_text.delete("1.0", "end")
        input_text.insert("1.0", decoded_data)

    else:
        input_text.delete("1.0", "end")
        input_text.insert("1.0", decoded_data)

# 再次解码按钮
again_decode_button = tk.Button(root, text="再次解码", command=again_decode)
again_decode_button.pack(side=tk.LEFT)

# 在同一行创建清空按钮，清空输入框的内容
clear_button = tk.Button(root, text="清空", command=lambda: input_text.delete("1.0", "end") and output_text.delete("1.0", "end"))
clear_button.pack(side=tk.LEFT)

# 创建帮助按钮
def help():
    messagebox.showinfo("帮助", "输入框内输入要编码或解码的内容，点击编码按钮进行编码，点击解码按钮进行解码。\n"
                                "对再次编码功能，若输出框有内容，则输出框的内容作为输入，否则用输入框作为输入，输出到输出框。\n"
                                "对再次解码功能，始终用输出框作为输入，解码完成后，结果同步输出到输出框和输入框。\n"
                                "点击清空按钮可以清空输入框和输出框的内容。")
help_button = tk.Button(root, text="帮助", command=help)
help_button.pack()

# 运行主循环
root.mainloop()

