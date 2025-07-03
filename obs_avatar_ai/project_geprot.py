import sys
import yaml
import logging
import threading
from pathlib import Path
from datetime import datetime
# Core constants
from core_config import OPENAI_API_KEY, TEXT_FILE_PATH, PERSONALITIES_DIR

import tkinter as tk
from tkinter import scrolledtext

import pyttsx3
from openai import OpenAI

# ——— Setup logging to file ————————————————————————————————
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ——— Select which personality config to load —————————————————————————
def select_config():
    files = list(Path(PERSONALITIES_DIR).glob("*.yaml"))
    if not files:
        print("No personality configs found.")
        sys.exit(1)
    print("Select Geprot's Personality:")
    print("-----------------------------")
    for idx, p in enumerate(files, 1):
        print(f"  {idx}: {p.name}")
    print("-----------------------------")
    try:
        choice = int(input("Enter choice: "))
        return files[choice - 1]
    except Exception:
        print("Invalid choice.")
        sys.exit(1)

# ——— Load YAML config ————————————————————————————————
def load_config(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        logging.error(f"Failed loading config {path}: {e}")
        print(f"Error loading config: {e}")
        sys.exit(1)

# ——— Initialize OpenAI client ————————————————————————————————
def init_openai():
    try:
        return OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        logging.error(f"OpenAI init failed: {e}")
        print("Could not initialize OpenAI. See error.log.")
        sys.exit(1)

# ——— Initialize TTS engine ————————————————————————————————
def init_voice_engine(voice_name: str):
    engine = pyttsx3.init()
    for v in engine.getProperty("voices"):
        if voice_name.lower() in v.name.lower():
            engine.setProperty("voice", v.id)
            return engine
    # fallback if not found
    logging.warning(f"Voice '{voice_name}' not found, using default.")
    return engine

# ——— Speak + Overlay ————————————————————————————————
def speak_and_overlay(engine, text: str):
    try:
        # Write to overlay text file
        Path(TEXT_FILE_PATH).write_text(text, encoding="utf-8")
    except Exception as e:
        logging.error(f"Failed writing overlay text: {e}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"TTS speaking failed: {e}")

# ——— GUI Chat ————————————————————————————————
def run_gui(cfg, client, model, engine, prompt_base):
    def on_send():
        user_text = entry.get().strip()
        if not user_text:
            return
        chat_log.insert(tk.END, f"You: {user_text}\n")
        chat_log.see(tk.END)
        entry.delete(0, tk.END)

        def fetch_reply():
            try:
                messages = [
                    {"role": "system", "content": prompt_base},
                    {"role": "user",   "content": user_text}
                ]
                resp = client.chat.completions.create(model=model, messages=messages)
                reply = resp.choices[0].message.content.strip()
                chat_log.insert(tk.END, f"{cfg['name']}: {reply}\n\n")
                chat_log.see(tk.END)
                speak_and_overlay(engine, reply)
            except Exception as e:
                logging.error(f"OpenAI API error: {e}")
                chat_log.insert(tk.END, "[ERROR] Failed to get AI response.\n")
                chat_log.see(tk.END)

        threading.Thread(target=fetch_reply, daemon=True).start()

    window = tk.Tk()
    window.title(f"Project Geprot — {cfg['name']}")
    window.geometry("600x500")

    chat_log = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='normal')
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry = tk.Entry(window)
    entry.pack(fill=tk.X, padx=10, pady=(0,10))
    entry.bind("<Return>", lambda e: on_send())
    entry.focus()

    send_btn = tk.Button(window, text="Send", command=on_send)
    send_btn.pack(pady=(0,10))

    window.mainloop()

# ——— Main ————————————————————————————————
if __name__ == "__main__":
    try:
        # 1. Choose and load config
        config_path = select_config()
        cfg = load_config(config_path)

        # 2. Init services
        client = init_openai()
        model = cfg.get("model", cfg.get("default_model", "gpt-4o"))
        engine = init_voice_engine(cfg.get("voice", "Microsoft David Desktop"))
        prompt_base = cfg.get("persona_prompt", f"You are {cfg['name']}.")

        # 3. Run GUI (no CLI fallback here for brevity)
        run_gui(cfg, client, model, engine, prompt_base)

    except Exception as fatal:
        logging.error("Fatal error in Project Geprot", exc_info=True)
        print("A critical error occurred. See error.log for details.")
