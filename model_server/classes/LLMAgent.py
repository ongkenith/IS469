from dotenv import load_dotenv
import os
from ollama import chat
import json
import re
from groq import Groq

# Load .env variables
load_dotenv()

class LLMAgent:
    def __init__(self):
        # self.main_model_name = "openai/gpt-oss-20b"
        self.main_model_name = "granite4.2:3b"
        self.effort_to_step_budget = {
            "Low": 1,
            "Medium": 3,
            "High": 5
        }
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

    def start_program(self, content, system_prompt, thinking_level = "Medium"):
        MAX_STEP_BUDGET = self.effort_to_step_budget[thinking_level]  # Maximum loops the harness will take to call the LLM
        WORKING_MEMORY = [system_prompt, f"[Start Point]: {content}\n"]
        
        step_budget = 0
        while step_budget < MAX_STEP_BUDGET:
            # Call orchestrator to determine the next step
            full_content = self.get_content_from_working_memory(WORKING_MEMORY)  # refresh every loop

            response = chat(
                model=self.main_model_name,
                format="json",  # forces valid JSON output
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': full_content},
                ],
                keep_alive="30m",
            )
            raw = response["message"]["content"]

            # response = self.client.chat.completions.create(
            #     model=self.main_model_name,
            #     response_format={"type": "json_object"},
            #     messages=[
            #         {'role': 'system', 'content': system_prompt},
            #         {'role': 'user', 'content': full_content},
            #     ],
            # )
            # raw = response.choices[0].message.content 
            action = self.parse_action(raw)

            if action is None:
                WORKING_MEMORY.append("[Error]: Output was not a valid JSON object\n")
                step_budget += 1
                print("Output not valid JSON object")

            else:
                kind = action.get("action")
                print(kind)

                # See what action orchestrator LLM want to do
                if kind == "Completed":
                    temp = re.sub(r"\[\w+\]:", "", WORKING_MEMORY[-1])
                    return temp.strip()

                elif kind == "call_specific_LLM":
                    task = action.get("type")
                    task_input = action.get("input", "")

                    if task == "Rephrase":
                        result = self.call_specific_LLM(f"Rephrase the following: {task_input}")
                        WORKING_MEMORY.append(f"[Rephrase]: {result}\n")
                    # elif task == "Critique":
                    #     ...
                    else:
                        WORKING_MEMORY.append(f"[Error]: Unknown task type '{task}'\n")
                else:
                    WORKING_MEMORY.append(f"[Error]: Unknown action '{kind}'\n")

                step_budget += 1

        return "Error: Ran out of step budget to answer the question"

    def call_specific_LLM(self, content, model="qwen3.5:0.8b"):
        response = chat(
            model=model,
            messages=[
                {'role': 'system', 'content': 'Do not ask for more clarifications. Produce only the necessary output'},
                {'role': 'user', 'content': content}
            ]
        )

        return response["message"]["content"]


text = ""
with open("Orchestrator.md", "r", encoding="utf-8") as f:
    text += f.read()

model = LLMAgent()
print(model.start_program("Fuck you. You have small eye that you cannot see your opponent and aim at them", text))