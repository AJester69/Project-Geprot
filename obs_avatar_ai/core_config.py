from pathlib import Path

# === OpenAI Settings ===
# Your real OpenAI API key goes here (or load via env).
OPENAI_API_KEY = "sk-"

# Default model for all chat calls
DEFAULT_MODEL = "gpt-4o"

# === File & Folder Paths ===
BASE_DIR = Path(__file__).resolve().parent
# Directory containing personality YAML files
PERSONALITIES_DIR = BASE_DIR / "personalities"
# Default overlay text file (written by TTS & read by overlay HTML)
DEFAULT_OVERLAY_FILE = BASE_DIR / "overlay_text.txt"

# === Memory Directory ===
# Folder where per-persona memory JSONL files are stored
MEMORY_DIR = BASE_DIR / "memory"

# === UI / Voice Defaults ===
# The default TTS voice if none is specified in a YAML
DEFAULT_VOICE = "Microsoft David Desktop"
