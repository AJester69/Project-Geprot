import sys
import yaml, time, re, threading
from pathlib import Path
from openai import OpenAI
import pyttsx3
import subprocess
import signal
import atexit

# === Load config file based on personality argument ===
profile = sys.argv[1] if len(sys.argv) > 1 else "dark_souls"
cfg_path = f"personalities/config_{profile}.yaml"

try:
    cfg = yaml.safe_load(Path(cfg_path).read_text(encoding="utf-8"))
except FileNotFoundError:
    print(f"❌ Config file not found: {cfg_path}")
    sys.exit(1)

# Launch overlay server in background
overlay_process = subprocess.Popen(
    ["python", "overlay_server.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW  # Hides the CMD window on Windows
)

# Ensure overlay server is closed when app exits
def cleanup():
    overlay_process.terminate()
    try:
        overlay_process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        overlay_process.kill()

atexit.register(cleanup)

# === Init services ===
ai    = OpenAI(api_key=cfg["openai_api_key"])
voice = pyttsx3.init()
voice.setProperty("rate", 175)
voice_name = cfg.get("voice", "").lower()

for v in voice.getProperty("voices"):
    if voice_name in v.name.lower():
        voice.setProperty("voice", v.id)
        break


# === Paths and config values ===
stats_path   = Path(cfg["stats_file"])
overlay_path = Path(cfg["overlay_file"])
name         = cfg["avatar_name"].lower()
prompt_base  = cfg["persona_prompt"]
interval     = cfg["poll_interval"]

# === Helpers ===
def parse_stats(txt):
    d, in_s = {}, False
    for L in txt.splitlines():
        if "[ Stats ]" in L: in_s=True; continue
        if "[" in L and "]" in L: in_s=False
        if in_s:
            m = re.match(r"([\w\s]+):\s+(\d+)", L)
            if m: d[m.group(1).strip()] = int(m.group(2))
    return d

def write_overlay(text):
    overlay_path.write_text(text, encoding="utf-8")

def speak(text):
    voice.say(text)
    voice.runAndWait()

# === Monitor for deaths (soul drop) ===
prev_stats = None
def monitor_deaths():
    global prev_stats
    while True:
        if stats_path.exists():
            txt = stats_path.read_text()
            cur = parse_stats(txt)
            if prev_stats and cur.get("Souls",0)==0 and prev_stats.get("Souls",0)>0:
                # Did other stats stay the same?
                ok = all(cur.get(k)==v for k,v in prev_stats.items() if k!="Souls")
                if ok:
                    msg = "Damn, mark another death."
                    write_overlay(msg)
                    speak(msg)
            prev_stats = cur
        time.sleep(interval)

# === Handle chat input ===
def command_loop():
    while True:
        line = input().strip()
        if line:
            question = line.strip()
            chat_in = [
                {"role": "system", "content": prompt_base},
                {"role": "user", "content": question}
            ]
            resp = ai.chat.completions.create(model="gpt-4o", messages=chat_in)
            out = resp.choices[0].message.content.strip()
            write_overlay(out)
            speak(out)

# === Entry Point ===
if __name__ == "__main__":
    write_overlay("")  # Clear old text
    threading.Thread(target=monitor_deaths, daemon=True).start()
    print(f"Geprot ready as '{profile}'. Type: {cfg['avatar_name']}, your question…")
    command_loop()
