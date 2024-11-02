import tkinter as tk
from tkinter import StringVar

def update_difference(*args):
    """Update the percentage difference as the values change."""
    try:
        value1 = float(entry_value1.get())
        value2 = float(entry_value2.get())
        difference = percentage_difference(value1, value2)
        result.set(f"百分差: {difference:.6f}%")
    except ValueError:
        result.set("请输入有效的数值")

def percentage_difference(value1, value2):
    """Calculate the percentage difference between two values."""
    difference = abs(value1 - value2)
    average = (value1 + value2) / 2
    if average == 0:
        return "不能除以零"
    percentage_difference = (difference / average) * 100
    return percentage_difference

# 创建Tkinter窗口
window = tk.Tk()
window.title("百分差计算器")
window.geometry('500x200')  # 设置窗口大小

# 设置字体和字号
font_family = '微软雅黑'
font_size = 24

# 创建输入框和标签
label_value1 = tk.Label(window, text="数值1", font=(font_family, font_size))
label_value1.grid(row=0, column=0)
entry_value1 = tk.Entry(window, font=(font_family, font_size))
entry_value1.grid(row=0, column=1)
entry_value1.bind('<KeyRelease>', update_difference)

label_value2 = tk.Label(window, text="数值2", font=(font_family, font_size))
label_value2.grid(row=1, column=0)
entry_value2 = tk.Entry(window, font=(font_family, font_size))
entry_value2.grid(row=1, column=1)
entry_value2.bind('<KeyRelease>', update_difference)

# 创建结果显示标签
result = StringVar()
label_result = tk.Label(window, textvariable=result, font=(font_family, font_size))
label_result.grid(row=2, column=0, columnspan=2)

# 运行Tkinter事件循环
window.mainloop()
