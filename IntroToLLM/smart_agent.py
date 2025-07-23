import ollama

class SmartAgent:
    def __init__(self, model):
        self.model_name = model
        with open("context_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
        self.chat_log = [{
        "role": "system",
        "content": system_prompt
        }
        ]
    def chat(self, message):
        self.chat_log.append({'role': 'user', 'content': message})
        answer = ollama.chat(
            model=self.model_name,
            messages=self.chat_log)
        answer_text = answer['message']['content']
        self.chat_log.append({'role': 'agent', 'content': answer_text})
        return answer_text
    