from classes.LayaClient import LayaClient

def predict_program(input_sentence):
    """ Start program and predicts sentiment of sentence """
    THRESHOLD_FOR_NON_OFFENSIVE = 0.95  # Set confidence percentage where result is non-offensive requires further checks

    laya_client = LayaClient()  # Call Client
    result = laya_client.is_message_offensive(input_sentence)  # Get the prediction

    if result["confidence"] > THRESHOLD_FOR_NON_OFFENSIVE and result["result"] == "0":  # If not offensive with high confidence
        print(f"[Laya LLM] Not offensive with {result['confidence']} confidence")
        return (input_sentence, 0)
    elif (result["confidence"] <= THRESHOLD_FOR_NON_OFFENSIVE and result["result"] == "0"):  # If offensive or not offensive but low confidence
        print(f"[Laya LLM] Not offensive with low ({result['confidence']}) confidence")
        return (input_sentence, 1)
    elif result["result"] == "1":  # If offensive or not offensive but low confidence
            print(f"[Laya LLM] Offensive phrasing")
            return (input_sentence, 1)
    else:
        print(f"[Laya LLM Error Exception] {result['result']}")
        return (input_sentence, -1)

    