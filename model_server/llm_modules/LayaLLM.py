import laya  

class LayaLLM:
    def __init__(self):     
        self.model_dir = "./laya_finetuned"
        try:
            self.agent = laya.load(self.model_dir)
        except:
            print("[LayaLLM Class Error]: Finetuned model cannot be loaded in. Reverting to basic model...")
            self.agent = laya.load("convaiinnovations/laya")
        
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
            print("Program is_message_offensive has started")
            res = self.agent.predict({"message": sentence}, self.questions)
            ans = res["answers"]["label"]

            print("Program is_message_offensive has ended")
            return {
                "result": str(ans["choice"]),
                "confidence": float(ans.get("answer_confidence"))
            }

        except Exception as e:
            print("Program is_message_offensive has started")
            return {
                "result": f"Error: {e}",
                "confidence": 0
            }