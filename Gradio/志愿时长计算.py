import gradio as gr


def calculate_time(sport, read, teach, learn):
    if sport > 15:
        time_sport = 0.5 * 15 + 0.33 * (sport - 15)
    else:
        time_sport = 0.5 * sport

    if read > 7:
        time_read = 0.5 * 7 + 0.33 * (read - 7)
    else:
        time_read = 0.5 * read

    if teach > 5:
        time_teach = 0.75 * 5 + 0.5 * (teach - 5)
    else:
        time_teach = 0.75 * teach

    if learn > 2:
        time_learn = 0.75 * 2 + 0.5 * (learn - 2)
    else:
        time_learn = 0.75 * learn

    total = round(time_sport + time_learn + time_teach + time_read, 2)
    total_str = str(total)+" 小时"

    return total_str


with gr.Blocks(theme="Soft") as Interface:
    with gr.Row():
        with gr.Column():
            in_sp = gr.Slider(label="云运动次数", minimum=0, step=1, maximum=22)
            in_re = gr.Slider(label="云阅读次数", minimum=0, step=1, maximum=26)
        with gr.Column():
            in_te = gr.Slider(label="云支教次数", minimum=0, step=1, maximum=17)
            in_le = gr.Slider(label="云研学次数", minimum=0, step=1, maximum=19)
    with gr.Row():
        cal_result = gr.Button("计算时长", variant="primary")
        out = gr.Textbox(show_label=False)

    cal_result.click(
        fn=calculate_time,
        inputs=[in_sp, in_re, in_te, in_le],
        outputs=out
    )

Interface.launch()