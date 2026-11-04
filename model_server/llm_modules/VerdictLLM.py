from ollama import chat

class VerdictLLM:
    def __init__(self):
        self.main_model_name = "qwen3"

    def get_verdict(self, content):
        """ Sends all the chat messages history, provide a verdict based on criteria """

        print("Program get_verdict has started")

        # Extract system prompt
        system_prompt = ""
        with open("./system_prompts/VerdictLLM.md", "r", encoding="utf-8") as f:
            system_prompt += f.read()

        response = chat(
            model=self.main_model_name,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': content}
                ]
            )

        res = response["message"]["content"]
        print(f"[LLM Verdict]: {res}")

        # Output safety check
        if res.strip() == "Others":
            print("Program get_verdict has ended")
            return {"verdict": "Other offenses beyond stated ones in our policy"}
        elif res.strip() not in ["Hate Speech", "Threats & Violence", "Sexual Content", "Harassment & Toxicity", "Scam & RMT", "Cheating Promotion", "Spam & Advertising", "Personal Information", "Impersonation"]:
            print("Program get_verdict has ended")
            return {"verdict": "Other offenses beyond stated ones in our policy"}

        print("Program get_verdict has ended")
        return {"verdict": res}