import pyttsx3
import logging
from pathlib import Path

class GeprotTTS:
    def __init__(self, voice_name: str, overlay_path: str):
        self.engine = pyttsx3.init()
        self.overlay_path = overlay_path
        self.set_voice(voice_name)

    def set_voice(self, voice_name: str):
        for v in self.engine.getProperty("voices"):
            if voice_name.lower() in v.name.lower():
                self.engine.setProperty("voice", v.id)
                return
        logging.warning(f"Voice '{voice_name}' not found, using default.")

    def speak_and_overlay(self, text: str):
        try:
            Path(self.overlay_path).write_text(text, encoding="utf-8")
        except Exception as e:
            logging.error(f"Failed writing overlay text: {e}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"TTS speaking failed: {e}")
