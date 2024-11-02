import os
import re
import send2trash
import gradio as gr

def find_files(directory, regex_pattern):
    pattern = re.compile(regex_pattern)
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern.search(file):
                matching_files.append(os.path.join(root, file))
    return os.linesep.join(matching_files), matching_files

def del_file(matching_files):
    for file in matching_files:
        send2trash.send2trash(file)
    return "文件已经移动到回收站"

with gr.Blocks() as interface:

    with gr.Row():
        regex_input = gr.Textbox(
            label="正则表达式",
            placeholder="在这里输入正则表达式",
            value=".+"  # 设置默认值为 .+
        )
        path_input = gr.Textbox(
            label="目录",
            placeholder="在这里输入目录",
        )
        search_btn = gr.Button("查找满足表达式的文件")

    file_list_display = gr.Textbox(
        label="找到的文件",
        interactive=False,
        placeholder="找到的文件会显示在这里",
        lines=5
    )
    file_list_state = gr.State([])

    with gr.Row():
        del_btn = gr.Button("删除文件")
        info = gr.Textbox(interactive=False, show_label=False)

    search_btn.click(
        fn=find_files,
        inputs=[path_input, regex_input],
        outputs=[file_list_display, file_list_state]
    )

    del_btn.click(
        fn=del_file,
        inputs=file_list_state,
        outputs=info
    )

interface.launch()
