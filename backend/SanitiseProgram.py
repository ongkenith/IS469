from classes.SanitiseAgentClient import SanitiseAgentClient

def sanitise_program(input_sentence):
    """ Start program and outputs santised sentiment of sentence """
    
    laya_client = SanitiseAgentClient()  # Call Client
    result = laya_client.sanitise_message(input_sentence)  # Get the prediction

    if "Error:" not in result["result"]:
        return (result["result"], 0)
    else:
        print(f"[Agent Error Exception] {result['result']}")
        return (input_sentence, -1)