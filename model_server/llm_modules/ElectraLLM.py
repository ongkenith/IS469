import time
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class ElectraLLM:
    BASE_MODEL = "google/electra-base-discriminator"

    def __init__(self):
        self.model_dir = "./electra_finetuned"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = 128

        # Label map (same meaning as the original criteria)
        self.id2label = {
            0: "not offensive: neutral, polite, or harmless message",
            1: "offensive: vulgar, insulting, hateful, abusive, threatening, or harassing message aimed at a person or group",
        }

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
            self.agent = AutoModelForSequenceClassification.from_pretrained(self.model_dir)
        except Exception:
            return Exception

        self.agent.to(self.device)
        self.agent.eval()

    def is_message_offensive(self, sentence):
        """ Inputs a sentence. Determines if sentence is offensive """

        if sentence is None or sentence.strip() == "":
            return {
                "result": "Error: Input is either empty or an empty string",
                "confidence": 0
            }

        try:
            print("Program is_message_offensive has started")
            start_time = time.perf_counter()

            inputs = self.tokenizer(
                sentence,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length,
            ).to(self.device)

            with torch.no_grad():
                logits = self.agent(**inputs).logits

            probs = torch.softmax(logits, dim=-1)[0]
            pred = int(torch.argmax(probs).item())
            confidence = float(probs[pred].item())

            end_time = time.perf_counter()
            print(f"Program is_message_offensive has ended. Time taken: {end_time-start_time}s")
            return {
                "result": str(pred),
                "confidence": confidence
            }

        except Exception as e:
            print("Program is_message_offensive has ended")
            return {
                "result": f"Error: {e}",
                "confidence": 0
            }