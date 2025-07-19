from openai import OpenAI
import json
import logging
from core_config import MEMORY_DIR

class GeprotChatEngine:
    @staticmethod
    def _slugify(name: str) -> str:
        return name.lower().replace(" ", "_")

    def __init__(self, api_key: str, model: str, system_prompt: str, persona_name: str):
        # 1) Init OpenAI client
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.persona_name = persona_name

        # 2) Ensure memory folder & determine file path
        MEMORY_DIR.mkdir(exist_ok=True)
        slug = self._slugify(persona_name)
        self.mem_file = MEMORY_DIR / f"{slug}.jsonl"

        # 3) Read existing history into lines
        history_lines = []
        if self.mem_file.exists():
            try:
                with open(self.mem_file, "r", encoding="utf-8") as f:
                    for line in f:
                        entry = json.loads(line)
                        speaker = "You" if entry["role"] == "user" else persona_name
                        history_lines.append(f"{speaker}: {entry['content']}")
            except Exception:
                logging.exception(f"Could not read memory for {persona_name}")

        # 4) Build one single system prompt: persona + history
        augmented_prompt = system_prompt
        if history_lines:
            augmented_prompt += "\n\n--- Previous conversation ---\n"
            augmented_prompt += "\n".join(history_lines)
            augmented_prompt += "\n--- End of history ---\n"

        self.message_history = [
            {"role": "system", "content": augmented_prompt}
        ]

    def send_message(self, user_input: str) -> str:
        # Append the user message
        self.message_history.append({"role": "user", "content": user_input})

        # Call OpenAI
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=self.message_history,
                temperature=0.7
            )
            reply = resp.choices[0].message.content.strip()
        except Exception:
            logging.exception("OpenAI API call failed in send_message")
            raise

        # Append & persist the assistant’s reply
        self.message_history.append({"role": "assistant", "content": reply})
        try:
            with open(self.mem_file, "a", encoding="utf-8") as f:
                f.write(json.dumps({"role":"user",      "content":user_input}, ensure_ascii=False)+"\n")
                f.write(json.dumps({"role":"assistant", "content":reply},      ensure_ascii=False)+"\n")
        except Exception:
            logging.exception(f"Failed writing memory file: {self.mem_file}")

        return reply
