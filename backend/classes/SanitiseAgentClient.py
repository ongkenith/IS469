import requests

class SanitiseAgentClient:
    def __init__(self, url="http://127.0.0.1:5001/agent_sanitise"):
        self.url = url

    def sanitise_message(self, sentence):
        """ Same return shape as SanitiseAgentClient.start_program """
        try:
            res = requests.post(self.url, json={"sentence": sentence})
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            return {"result": f"Error: {e}"}