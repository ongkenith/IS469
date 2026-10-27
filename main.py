import sys
from SanitiseProgram import sanitise_program

# Configuration Variables
REMOVE_LLM_THINKING_PRINT_STATEMENTS = False

def main():
    """ Main function executed when Python CLI executed"""
    global REMOVE_LLM_THINKING_PRINT_STATEMENTS

    args = sys.argv[1:]
    if "--remove-LLM-thinking" in args:  # If user decides to not see intermediate steps
        REMOVE_LLM_THINKING_PRINT_STATEMENTS = True

    print("=== Program Starting Up... ===\n")  # Starting Up

    try:
        while True:
            input_sentence = input("Type your sentence here: ")

            # Check if input is empty
            while input_sentence.strip() == "":
                input_sentence = input("Type your sentence here (empty string not accepted): ")

            # Call program Function
            sanitise_program(input_sentence, llm_intermediate_statement=REMOVE_LLM_THINKING_PRINT_STATEMENTS)

            # Check if User wants to end it
            input_continue_program = input("Do you have other sentences? (Y/N): ")
            if input_continue_program.strip() == "N" or input_continue_program.strip() == "n":
                break

        print("\n=== End of Program ===")
        
    except KeyboardInterrupt:
        print("\n=== End of Program ===")

if __name__ == "__main__":
    main()