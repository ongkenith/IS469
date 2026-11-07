from dotenv import load_dotenv
import os
from ollama import chat
import json
import re
from groq import Groq

# Load .env variables
load_dotenv()

class RephraseAgent:
    def __init__(self):
        self.main_model_name = "openai/gpt-oss-20b"
        self.effort_to_step_budget = {
            "Low": 2,
            "Medium": 4,
            "High": 6
        }
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.logs = []

    def get_content_from_working_memory(self, working_memory):
        """ To concatenate the content from working memory """
        return "".join(working_memory[1:])

    def parse_action(self, raw):
        """Safely parse the orchestrator's output. Returns a dict or None."""
        try:
            action = json.loads(raw)
        except json.JSONDecodeError:
            return None
        return action if isinstance(action, dict) else None

    def get_system_prompt_from_md_file(self, filename):
        """ Get instructions from MD file """
        system_prompt = ""
        with open(filename, "r", encoding="utf-8") as f:
            system_prompt += f.read()

        return system_prompt

    def start_program(self, content):
        print("Program start_program has started")
        system_prompt = self.get_system_prompt_from_md_file("./system_prompts/RephraseOrchestrator.md")  # Get system prompt instructions
        try:  # Get thinking effort for agent
            thinking_level = os.getenv("THINKING_EFFORT")
        except:
            thinking_level = "Medium"

        MAX_STEP_BUDGET = self.effort_to_step_budget[thinking_level]  # Maximum loops the harness will take to call the LLM
        MAX_ERROR_RETRIES = 2  # Maximum times the LLM can retry
        WORKING_MEMORY = [system_prompt, f"[Start Point]: {content}\n"]
        
        step_budget = 0
        error_retires = 0
        while step_budget < MAX_STEP_BUDGET:
            # Early break if retired too many times
            if error_retires >= MAX_ERROR_RETRIES:
                return "Error: LLM did too many retries to answer the question"

            # Call orchestrator to determine the next step
            full_content = self.get_content_from_working_memory(WORKING_MEMORY)  # refresh every loop

            # Using GROQ
            response = self.client.chat.completions.create(
                model=self.main_model_name,
                response_format={"type": "json_object"},
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': full_content},
                ],
            )
            raw = response.choices[0].message.content 

            self.logs.append(f"> Orchestrator -- '{raw}'")
            action = self.parse_action(raw)

            if action is None:
                WORKING_MEMORY.append("[Error]: Output was not a valid JSON object\n")
                error_retires += 1
                self.logs.append(f"> Step Budget: {step_budget}, Retries: {error_retires} -- 'Output not valid JSON object'")

            else:
                kind = action.get("action")

                # See what action orchestrator LLM want to do
                if kind == "Completed":
                    if re.sub(r"\[[^\]]+\]\:", "", WORKING_MEMORY[-1].strip()).strip() == "":
                        self.logs.append(f"> Return -- 'LLM did not return anything'")

                        print("Program start_program has ended")
                        print("\n".join(self.logs))
                        
                        return {"result": "Error: LLM did not return anything"}
                    temp = re.sub(r"\[[^\]]+\]\:", "", WORKING_MEMORY[-1].strip())
                    if '"' in temp[0]: temp = temp[1:len(temp)-1]
                    elif '“' in temp[0]: temp = temp[1:len(temp)-1]
                    self.logs.append(f"> Return -- '{temp}'")

                    print("Program start_program has ended")
                    print("\n".join(self.logs))
                    
                    return {"result" : temp.strip()}

                elif kind == "call_specific_LLM":
                    task = action.get("type")
                    task_input = action.get("input", "")

                    if task == "Rephrase":
                        result = self.call_rephraser_LLM(f"Rephrase the following: {task_input}").strip()
                        WORKING_MEMORY.append(f"[Rephrase]: {result}\n")
                        step_budget += 1
                        self.logs.append(f"> Step Budget: {step_budget}, Retries: {error_retires} -- '{result}'")
                    else:
                        error_retires += 1
                        WORKING_MEMORY.append(f"[Error]: Unknown task type '{task}'\n")
                        self.logs.append(f"> Step Budget: {step_budget}, Retries: {error_retires} -- 'Unknown task type '{task}''")
                else:
                    error_retires += 1
                    WORKING_MEMORY.append(f"[Error]: Unknown action '{kind}'\n")
                    self.logs.append(f"> Step Budget: {step_budget}, Retries: {error_retires} -- 'Unknown action '{kind}''")

        print("Program start_program has ended")
        print("\n".join(self.logs))
        return {"result": "Error: Ran out of step budget to answer the question"}

    def call_rephraser_LLM(self, content, model="gemma3:4b"):
        system_prompt = self.get_system_prompt_from_md_file("./system_prompts/RephraseLLM.md")

        response = chat(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': content}
            ]
        )

        return response["message"]["content"]