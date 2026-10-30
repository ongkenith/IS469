import requests

class LayaClient:
    def __init__(self, url="http://127.0.0.1:5001/laya_predict"):
        self.url = url

    def is_message_offensive(self, sentence):
        """ Same return shape as LayaLLM.is_message_offensive """
        try:
            res = requests.post(self.url, json={"sentence": sentence})
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            return {"result": f"Error: {e}", "confidence": 0}