class SanitiseProgram:
    """ Class for the program """

    def __init__(self, llm_intermediate_statement=True):
        self.DISPLAY_LLM_INTERMEDIATE_STATEMENT = llm_intermediate_statement
        self.input_sentence = ""

    def add_input_sentence(self, input_sentence):
        """ Add input sentence required for sanitisation """
        # Some cleaning and input checks?   
        self.input_sentence = input_sentence