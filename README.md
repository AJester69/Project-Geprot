diff --git a/README.md b/README.md
index 2768126c4ed347b46617ae2e4286a59a1d4d8e03..bd642cedc68f57fb5d80764aafbb2bd45d3ba7ec 100644
--- a/README.md
+++ b/README.md
@@ -6,29 +6,42 @@ An AI-driven streaming companion with a unified GUI chat interface, OBS overlay
 
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
+- **Dependencies**
   ```bash
   pip install openai pyttsx3 pyyaml
+  ```
+
+After installing dependencies, start the overlay server in one terminal:
+
+```bash
+python obs_avatar_ai/overlay_server.py
+```
+
+Then run the main application in another terminal:
+
+```bash
+python obs_avatar_ai/project_geprot.py
+```
 
