import gradio as gr
from datetime import datetime
import pyperclip

# 计算距离的函数
def calculate_distance(speed, hour, minute, second):
    try:
        # 将时间字符串转换为datetime对象
        time_string = f"{hour:02d}:{minute:02d}:{second:02d}"
        time_format = "%H:%M:%S"
        time_delta = datetime.strptime(time_string, time_format) - datetime.strptime("00:00:00", time_format)

        # 计算时间差的总秒数
        total_seconds = time_delta.total_seconds()

        # 计算距离（速度*时间，时间以小时为单位）
        distance = speed * (total_seconds / 3600)

        return f"{distance:.2f} km"
    except ValueError:
        return "请输入正确的速度和时间格式"

def copy_result(result):
    pyperclip.copy(result)
    return "成功复制到剪贴板"

# 创建Gradio界面
with gr.Blocks() as iface:
    gr.Markdown("# 计算距离")
    with gr.Row():
        with gr.Column():
            input_hour = gr.Slider(minimum=0, maximum=23, step=1, label="小时")
            input_minute = gr.Slider(minimum=0, maximum=59, step=1, label="分钟")
            input_second = gr.Slider(minimum=0, maximum=59, step=1, label="秒")
            input_speed = gr.Number(label="速度（千米/小时）")
            calculate_button = gr.Button("计算")
        with gr.Column():
            output_distance = gr.Textbox(label="距离", interactive=False)
            with gr.Row():
                copy_result_button = gr.Button("复制结果")
                copy_info = gr.Textbox(interactive=False, label="日志", show_label=False)

    calculate_button.click(
        fn=calculate_distance,
        inputs=[input_speed, input_hour, input_minute, input_second],
        outputs=output_distance
    )

    copy_result_button.click(
        fn=copy_result,
        inputs=output_distance,
        outputs=copy_info
    )

# 启动Gradio应用
iface.launch()
