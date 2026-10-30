import laya  

class LayaLLM:
    def __init__(self):     
        self.model = "convaiinnovations/laya"
        self.agent = laya.load(self.model)
        
        # Set up the structure and prompt for Laya LLM
        self.questions = {
            "label": {
                "type": "choice",
                "instructions": "Is this message offensive?",
                "criteria": {
                    "0": "not offensive: neutral, polite, or harmless message",
                    "1": "offensive: vulgar, insulting, hateful, abusive, threatening, or harassing message aimed at a person or group",
                },
            }
        }

    def is_message_offensive(self, sentence):
        """ Inputs a sentence. Determines if sentence is offensive """

        if sentence.strip() == "":
            return {
                "result": "Error: Input is either empty or an empty string",
                "confidence": 0
            }

        try: 
            res = self.agent.predict({"message": sentence}, self.questions)
            ans = res["answers"]["label"]

            return {
                "result": str(ans["choice"]),
                "confidence": float(ans.get("answer_confidence"))
            }

        except Exception as e:
            return {
                "result": f"Error: {e}",
                "confidence": 0
            }