import sys
import yaml
import logging
import threading
from pathlib import Path
from datetime import datetime

# Core constants
from core_config import (
    OPENAI_API_KEY,
    DEFAULT_MODEL,
    PERSONALITIES_DIR,
    DEFAULT_OVERLAY_FILE,
    DEFAULT_VOICE
)

import tkinter as tk
from tkinter import scrolledtext

from engine.tts_engine import GeprotTTS
from engine.chat_engine import GeprotChatEngine

def select_config():
    files = list(Path(PERSONALITIES_DIR).glob("*.yaml"))
    if not files:
        print("No personality configs found.")
        sys.exit(1)
    print("Select Geprot's Personality:")
    print("-----------------------------")
    for idx, p in enumerate(files, 1):
        print(f"  [{idx}] {p.name}")
    print("-----------------------------")
    try:
        choice = int(input("Enter number: "))
        return files[choice - 1]
    except Exception:
        print("Invalid choice.")
        sys.exit(1)

def load_config(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        logging.error(f"Failed loading config {path}: {e}")
        print(f"Error loading config: {e}")
        sys.exit(1)

def run_gui(cfg, chat_engine, tts):
    def on_send():
        user_text = entry.get().strip()
        if not user_text:
            return
        chat_log.insert(tk.END, f"You: {user_text}\n")
        chat_log.see(tk.END)
        entry.delete(0, tk.END)

        def fetch_reply():
            try:
                reply = chat_engine.send_message(user_text)
                chat_log.insert(tk.END, f"{cfg.get('name')}: {reply}\n\n")
                chat_log.see(tk.END)
                tts.speak_and_overlay(reply)
            except Exception:
                logging.exception("Error in fetch_reply")
                chat_log.insert(tk.END, "[ERROR] Failed to get AI response.\n")
                chat_log.see(tk.END)

        threading.Thread(target=fetch_reply, daemon=True).start()

    try:
        window = tk.Tk()
    except Exception:
        logging.exception("Failed to initialize Tkinter GUI")
        raise

    window.title(f"Project Geprot — {cfg.get('name')}")
    window.geometry("600x500")

    chat_log = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='normal')
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry = tk.Entry(window)
    entry.pack(fill=tk.X, padx=10, pady=(0,10))
    entry.bind("<Return>", lambda e: on_send())
    entry.focus()

    send_btn = tk.Button(window, text="Send", command=on_send)
    send_btn.pack(pady=(0,10))

    # Pre-populate history
    for msg in chat_engine.message_history:
        if msg['role'] == 'system':
            continue
        speaker = 'You' if msg['role'] == 'user' else cfg.get('name')
        chat_log.insert(tk.END, f"{speaker}: {msg['content']}\n\n")
    chat_log.see(tk.END)

    window.mainloop()

def main():
    # — Quick startup logging
    logging.error("===== Project Geprot starting =====")
    logging.error(f"Working directory: {Path.cwd()}")
    logging.error(f"sys.argv: {sys.argv}")

    # 1. Load config (allow CLI override)
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    else:
        config_path = select_config()
    logging.error(f"Selected config_path: {config_path}")

    cfg = load_config(config_path)
    logging.error(f"Config loaded: {cfg.get('name', cfg.get('avatar_name'))}")

    # 2. Init services
    model = cfg.get("model", DEFAULT_MODEL)
    name = cfg.get("name", cfg.get("avatar_name", "Geprot"))
    system_prompt = cfg.get("persona_prompt", f"You are {name}.")

    chat_engine = GeprotChatEngine(
        api_key=OPENAI_API_KEY,
        model=model,
        system_prompt=system_prompt,
        persona_name=name,
    )

    overlay_path = cfg.get("overlay_file", DEFAULT_OVERLAY_FILE)
    tts = GeprotTTS(cfg.get("voice", DEFAULT_VOICE), overlay_path)

    # 3. Run GUI
    run_gui(cfg, chat_engine, tts)

if __name__ == "__main__":
    # This block only runs when calling project_geprot.py directly
    try:
        main()
    except Exception:
        logging.exception("Fatal error in Project Geprot")
        print("A critical error occurred. See error.log for details.")
