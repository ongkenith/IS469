import requests

class VerdictLLMClient:
    def __init__(self, url="http://127.0.0.1:5001/llm_verdict"):
        self.url = url

    def get_verdict(self, chat_history):
        try:
            res = requests.post(self.url, json={"chat_history": chat_history})
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            return {"verdict": f"Error: {e}"}