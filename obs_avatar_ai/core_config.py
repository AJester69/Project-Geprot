# core_config.py

from pathlib import Path

# === API Key (centralized) ===
OPENAI_API_KEY = "sk-"
DEFAULT_MODEL = "gpt-4o"

# Folder Paths
BASE_DIR = Path(__file__).resolve().parent
SPRITE_PATH = BASE_DIR / "paladin_sprite.gif"
TEXT_FILE_PATH = BASE_DIR / "overlay_text.txt"
ERROR_LOG_PATH = BASE_DIR / "error.log"
PERSONALITIES_DIR = BASE_DIR / "personalities"

# Overlay
OVERLAY_PORT = 5005
MAX_DISPLAY_WORDS = 10  # max words visible in avatar bubble

# LLM Config
DEFAULT_MODEL = "gpt-4o"
TTS_RATE = 200  # default speech rate

# Application
APP_LAUNCH_SCRIPT = BASE_DIR / "project_geprot.py"
OVERLAY_SCRIPT = BASE_DIR / "overlay_server.py"
SPRITE_FILENAME = "paladin_sprite.gif"

# GUI Defaults
FONT_NAME = "Arial"
FONT_SIZE = 12
WINDOW_TITLE = "Geprot Interface"

# Overlay Appearance
OVERLAY_WIDTH = 400
OVERLAY_HEIGHT = 200
TEXT_FADE_DELAY = 10

# Voice (pyttsx3 base)
VOICE_NAME = "Microsoft David Desktop - English (United States)"
