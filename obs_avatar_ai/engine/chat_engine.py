from openai import OpenAI

class GeprotChatEngine:
    def __init__(self, api_key: str, model: str, system_prompt: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.message_history = [{"role": "system", "content": system_prompt}]

    def send_message(self, user_input: str) -> str:
        self.message_history.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.message_history,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        self.message_history.append({"role": "assistant", "content": reply})

        return reply
