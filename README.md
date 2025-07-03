# Project Geprot v0.2

An AI-driven streaming companion with a unified GUI chat interface, OBS overlay integration, and extensible character “personalities.” Configure your favorite in-character helper (e.g. Solaire of Astora, Tirion Fordring) via simple YAML files and let Geprot speak, reply, and update your stream overlay in real time.

---

## 🚀 Features

- **Unified GUI + CLI fallback**  
  Primary interface built in Tkinter; if it fails, a console chat mode remains available for debugging.

- **Config-driven personalities**  
  Swap “characters” by picking from `personalities/*.yaml`. Each defines name, prompt, model, and preferred TTS voice.

- **OBS Overlay integration**  
  Geprot writes its latest reply to `overlay_text.txt`, which `overlay_server.py` serves on a browser source in OBS.

- **Text-to-speech**  
  Voices via `pyttsx3`—configured per personality, with safe fallback if the chosen voice isn’t installed.

- **Robust error‐handling**  
  All unexpected errors (TTS, overlay, OpenAI API) log to `error.log` without crashing the UI.

---

## 📦 Getting Started

### Requirements

- **Python 3.8+**  
- **Dependencies**
  ```bash
  pip install openai pyttsx3 pyyaml
  ```

After installing dependencies, start the overlay server in one terminal:

```bash
python obs_avatar_ai/overlay_server.py
```

Then run the main application in another terminal:

```bash
python obs_avatar_ai/project_geprot.py
```

