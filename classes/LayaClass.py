class LayaLLM:
    def __init__(self, sentence):
        import laya
        
        self.sentence = sentence
        self.model = "convaiinnovations/laya"
        
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