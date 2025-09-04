import gradio as gr
from calc import calc_money


def process_lines(footy_notes):
    lines = footy_notes.split('\n')
    return calc_money(lines)


if __name__ == "__main__":
    with open('fixtures-all-2024.txt') as f:
        default = f.read()
    input = gr.Textbox(value=default, label="Enter footy notes")
    demo = gr.Interface(fn=process_lines, inputs=input, outputs="textbox")
    demo.launch()
