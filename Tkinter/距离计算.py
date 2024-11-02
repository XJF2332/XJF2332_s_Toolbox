import tkinter as tk
from datetime import datetime


# 计算距离的函数
def calculate_distance(*args):
    try:
        # 获取用户输入的速度和时间
        speed = float(speed_entry.get())
        time_str = time_entry.get()

        # 将时间字符串转换为datetime对象
        time_format = "%H:%M:%S"
        time_delta = datetime.strptime(time_str, time_format) - datetime.strptime("00:00:00", time_format)

        # 计算时间差的总秒数
        total_seconds = time_delta.total_seconds()

        # 计算距离（速度*时间，时间以小时为单位）
        distance = speed * (total_seconds / 3600)

        # 更新距离显示
        distance_label.config(text=f"距离: {distance:.2f} 千米")
    except ValueError:
        distance_label.config(text="请输入正确的速度和时间格式")


# 创建主窗口
root = tk.Tk()
root.title("距离计算器")

# 创建并放置输入框和标签
tk.Label(root, text="平均速度（千米/时）:").grid(row=0, column=0)
speed_entry = tk.Entry(root)
speed_entry.grid(row=0, column=1)

tk.Label(root, text="时间（时:分:秒）:").grid(row=1, column=0)
time_entry = tk.Entry(root)
time_entry.grid(row=1, column=1)

# 创建距离显示标签
distance_label = tk.Label(root, text="距离: 0.00 千米")
distance_label.grid(row=2, column=0, columnspan=2)

# 绑定输入框内容变化事件
speed_entry.bind('<KeyRelease>', calculate_distance)
time_entry.bind('<KeyRelease>', calculate_distance)

# 运行主循环
root.mainloop()
