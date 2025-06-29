# Project Geprot

**Project Geprot** is a modular AI-powered virtual companion system designed for streamers. It integrates character-based personalities, voice responses, chat interactions, and visual overlays in OBS — all customizable through config files and easy toggling via a GUI or .bat launcher.

> Originally designed to accompany a Dark Souls playthrough as "Geprot the Paladin," this system supports modular personalities, file-based game interaction, and fully voice-acted feedback.

---

## 🛠 Features

- 🎭 **Modular Personality System**
  - Choose from character configs (e.g. Solaire, Tirion) with unique voices and tone
  - Triggerable by name or globally as "Geprot"

- 🧠 **ChatGPT-Driven Dialogue**
  - Powered by OpenAI’s API (GPT-4o or other models)
  - Interacts with typed questions via a custom GUI

- 🔈 **Voice Output**
  - Configurable with built-in Windows voices (Zira, David, etc.)
  - Optional future integration with ElevenLabs or custom TTS engines

- 🎥 **Stream Overlay Integration**
  - Renders a GIF avatar loop + speech bubble via OBS browser source
  - Outputs response text to `overlay_text.txt` in real-time

- 📂 **File-based Game Interaction**
  - Optionally monitors `.txt` files for in-game stats (e.g. player death or soul changes)
  - Reacts dynamically during gameplay

---

## 📁 Folder Structure

```
obs_avatar_ai/
├── app.py                 # Legacy terminal version (still supported)
├── gui_app.pyw            # GUI front-end for user interaction
├── geprot_core.py         # (Planned) Shared logic for speaking, overlay, and personality setup
├── overlay_server.py      # Serves overlay_text.txt to OBS
├── overlay_text.html      # OBS browser overlay template (with GIF + speech bubble)
├── launch_geprot.bat      # Menu-driven launcher to pick a personality
├── overlay_text.txt       # Generated speech bubble text for OBS
├── personalities/         # Folder containing character config files
│   ├── config_dark_souls.yaml   # Solaire of Astora personality
│   └── config_warcraft.yaml     # Tirion Fordring personality
```

---

## 🧠 Personalities

Each personality is stored in a YAML file under `/personalities/`, e.g.:
- `config_dark_souls.yaml` → Responds as *Solaire*
- `config_warcraft.yaml` → Responds as *Tirion Fordring*

YAML keys include:
```yaml
name: Solaire
trigger: solaire
voice: Microsoft David Desktop
personality: Cheerful, sun-worshipping paladin from Dark Souls...
```

---

## 🖥 Requirements

- Python 3.10+
- [OpenAI Python SDK](https://pypi.org/project/openai/)
- `pyttsx3` for voice output
- `tkinter` (bundled with Python)
- OBS (optional, for overlay display)

Install packages:
```bash
pip install openai pyttsx3
```

---

## 🚀 How to Launch

1. Double-click `launch_geprot.bat`
2. Select personality
3. GUI window launches for input
4. Overlay auto-starts and displays avatar & speech bubble in OBS

> Tip: Add `overlay_text.html` to OBS as a browser source pointing to `http://localhost:8000/overlay_text.html`.

---

## 🛠 Planned Upgrades

- React live to game save files (e.g., deaths, location)
- Personality memory & progression
- Support for voice activation (keyword-based or push-to-talk)
- Swappable avatars per config
- Better voice fidelity (via ElevenLabs or Bark)

---

## 🔐 Notes

- This project is private, but ready for modular expansion
- Voice and API key handling is local — no user data is sent externally except to OpenAI
- Use responsibly on stream (especially if using audio triggers)

---

## 📇 Credits

Built and maintained by [AJester](https://www.twitch.tv/ajester69ttv) with AI co-development.
