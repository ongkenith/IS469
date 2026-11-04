from classes.VerdictLLMClient import VerdictLLMClient

def get_verdict(chat_history):
    
    client = VerdictLLMClient()  # Call Client
    result = client.get_verdict(chat_history)  # Get the prediction

    if "Error:" not in result["verdict"]:
        return (result["verdict"], 0)
    else:
        print(f"[LLM Error Exception] {result['verdict']}")
        return (None, -1)