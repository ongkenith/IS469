from classes.LayaClass import LayaLLM
import laya

# Load Laya LLM model that will be used
_model = LayaLLM()

def sanitise_program(input_sentence):
    """ Start program and outputs santised sentiment of sentence """
    THRESHOLD_FOR_NON_OFFENSIVE = 0.15  # Set confidence percentage where result is non-offensive requires further checks

    # Call LLM and get the prediction
    model = LayaLLM()
    result = model.is_message_offensive(input_sentence)

    if result["confidence"] > THRESHOLD_FOR_NON_OFFENSIVE and result["result"] == "0":  # If not offensive with high confidence
        print(f"[Laya LLM] Not offensive with {result['confidence']} confidence")
        return (input_sentence, 0)
    elif (result["confidence"] <= THRESHOLD_FOR_NON_OFFENSIVE and result["result"] == "0") or result["result"] == "1":  # If offensive or not offensive but low confidence
        print(f"[Laya LLM] Not offensive with {result['confidence']} confidence / Offensive")
        return (input_sentence, 1)
    else:
        print(f"[Laya LLM Error Exception] {result['result']}")
        return (input_sentence, -1)

    