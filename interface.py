import gradio as gr
import pandas as pd

last_dataframe = None

def chatbot(message, history):
    global last_dataframe
    if "table" in message.lower():
        df = pd.read_csv('Iphone 16.csv', encoding='utf-16')
        history.append((message, "Here’s your table → see right panel"))
        last_dataframe = df
        return history, last_dataframe
    else:
        history.append((message, f"Echo: {message}"))
        return history, last_dataframe

def download_csv():
    global last_dataframe
    if last_dataframe is not None:
        path = "output.csv"
        last_dataframe.to_csv(path, index=False)
        return path
    return None

def download_excel():
    global last_dataframe
    if last_dataframe is not None:
        path = "output.xlsx"
        last_dataframe.to_excel(path, index=False)
        return path
    return None

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=2):
            chatbot_ui = gr.Chatbot(max_height="80vh")
            msg = gr.Textbox(
                label="Your message",
                placeholder="Type here..."
            )
            with gr.Row():
                send_btn = gr.Button("Send")
                clear_btn = gr.Button("Clear Chat")

        with gr.Column(scale=2):
            df_display = gr.Dataframe(
                interactive=True,
                wrap=True
            )
            with gr.Row():
                download_csv_btn = gr.DownloadButton("Download CSV")
                download_excel_btn = gr.DownloadButton("Download Excel")

    # Wiring
    msg.submit(chatbot, inputs=[msg, chatbot_ui], outputs=[chatbot_ui, df_display])
    send_btn.click(chatbot, inputs=[msg, chatbot_ui], outputs=[chatbot_ui, df_display])
    clear_btn.click(lambda: [], None, chatbot_ui)

    download_csv_btn.click(download_csv, None, download_csv_btn)
    download_excel_btn.click(download_excel, None, download_excel_btn)

demo.launch()
