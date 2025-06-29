import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path
import yaml
import openai
import os

# Load config
cfg_path = Path(__file__).parent / os.sys.argv[1]
cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

# Set up OpenAI
ai = openai.OpenAI(api_key=cfg["openai_api_key"])
model = cfg.get("model", "gpt-4o")
prompt_base = f"You are {cfg['name']}. Respond in character as a paladin.\n"

# Set up window
window = tk.Tk()
window.title(f"Geprot ({cfg['name']})")
window.geometry("600x500")

# Top chat log
chat_log = scrolledtext.ScrolledText(window, wrap=tk.WORD, state="disabled", bg="#1e1e1e", fg="#dcdcdc", font=("Consolas", 11))
chat_log.pack(padx=10, pady=(10, 5), fill=tk.BOTH, expand=True)

# Frame for bottom input and button
input_frame = tk.Frame(window)
input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

# Input box
user_input = tk.Entry(input_frame, font=("Consolas", 11))
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

# Send button
def send_input(event=None):
    user_text = user_input.get().strip()
    if not user_text:
        return
    append_to_chat_log("You", user_text)
    user_input.delete(0, tk.END)

    messages = [
        {"role": "system", "content": prompt_base},
        {"role": "user", "content": user_text}
    ]
    try:
        response = ai.chat.completions.create(model=model, messages=messages)
        reply = response.choices[0].message.content.strip()
        append_to_chat_log(cfg["name"], reply)
    except Exception as e:
        append_to_chat_log("System", f"[Error] {e}")

send_button = tk.Button(input_frame, text="Send", command=send_input)
send_button.pack(side=tk.RIGHT)

# Allow pressing Enter to send
user_input.bind("<Return>", send_input)

# Output formatter
def append_to_chat_log(speaker, message):
    chat_log.configure(state="normal")
    chat_log.insert(tk.END, f"{speaker}: {message}\n\n")
    chat_log.configure(state="disabled")
    chat_log.see(tk.END)

# Launch GUI
window.mainloop()
