# IS469 Project: Offensive Message Detection & Rephrasing
Using Artifical Intelligence (AI) (Large Language Models (LLMs), System One Decision Model / Encoder Model etc.) to detect offensive messages and suggest respectful rephrasings that preserve the sender's original intent.

### Overview ###
This project explores with **NO** dataset to train on, how a non-autoregressive System One decision model can be used to flag offensive or toxic messages.
> Options are available to use a fine-tuned System One decision model or an older encoder model to do the classification

This project also extends to the following:
- using Agentic AI to automatically rewrite them in a more constructive tone while maintaining the message, instead of relying on ban word list OR pattern matching like Regex, to mask messages with asterisk.
- using LLM to identify the policy violated by the player

## Pre-requisites
Ensure that the following are installed on your device before running the Backend, Frontend and Model_Server's services:
- Next.js v16.4.3 or latest most stable and safe version
- Python v3.12 or higher
- Ollama installed and currently running locally
- GROQ API key

## Installation Guide
1. **Install Python dependencies**
```bash
python -m pip install -r requirements.txt
```
2. **Install NextJS dependencies**
```bash
cd frontend
npm install
```
3. **Pull the following Ollama model(s)**
```bash
ollama pull gemma3:4b
ollama pull qwen3
```
4. **Set up environment variables**<br>
    1. Make a copy of .env.example file under 'model_server' folder
    2. Add your GROQ API key
    3. Adjust THINKING_EFFORT you want the Agent to have (Low, Medium or High)
    4. Adjust THRESHOLD_FOR_NON_OFFENSIVE to determine how low of a confidence score will require non-offensive classification to be redirected to an LLM

### OPTIONAL: Add a finetuned model

Inside 'training materials' folder, there are a few notebooks to train either: 
- 'laya_model_training_notebook.ipynb' to train Laya model 
- 'electra_model_training_notebook.ipynb' to train ELECTRA model

Together with the processed dataset, run the required cells to **train**, **evaluate** and extract the model's weights to a folder.<br>
Rename the folder to either "laya_finetuned" OR "electra_finetuned" and add it in the "model_server" directory.

Otherwise, the default Laya base model will be used (convaiinnovations/laya)

<b>ANY OTHER MODEL MAY REQUIRE CODE CHANGES!</b>

## Running the Application
**Step 1**<br>
Open up Ollama desktop application and ensure it is running in the background

**Step 2**<br>
Start each service in a separate terminal:

```bash
# Terminal 1: Model Server 
cd model_server
python model_server.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Step 3**<br>
Once these two terminals have started successfully, open another new terminal:
```bash
# Terminal 3: Backend
cd backend
python main.py
```

The app will be available at `http://localhost:3000`.

Refer to command line to see the printed logs of the application.

## Demo
**Home Page - Chat Interface to Simulate the project**<br>
<img src='README_assets/homepage.png' width='50%' alt='Img of Home Page' />
- Press on "Start Chat" to begin typing a message
- Press "Send" to send the message. The message will take a while to display as it is going through the AI to check if it is offensive<br>

**Status of the Message**<br>
<img src='README_assets/message_status.png' width='50%' alt='Message Status' />
- If message has been checked and is not offensive, it will be displayed as normal
- If message has been checked and is offensive, it will display the rephrased version. Asterisk at the start and end of the message will also indiciate the sentence has been rephrased. *Default* rephrasing is "Message is offensive" if Agent runs out of step budget.
- If message is under scrutinisation by the AI, it will display '[Your message is being rewritten...]' as a placeholder

**Warning Message for Offensive Chat Session**<br>
If during the chat session has been flagged as offensive, a warning message (in red) will be displayed below the chat.<br>
<img src='README_assets/warning_message.png' width='50%' alt='Offensive Warning' />


## Limitations of Applications
**Limitation 1:** Reliance on Third-party Services<br>
The orchestrator agent uses an open-weight model hosted by GROQ, a third party company. Therefore, it is subjected to the limits of API calling, as well as hosting support of the model used in this application
>**Mitigation**: If support discontinues, the frontend will treat all non-error code 200 to be rephrased to '*Message is offensive*'

**Limitation 2:** Quality of Rephrased Sentence<br>
The quality of the rephrased sentence is dependent on whether the orchestrator believes it passes the criteria it was given. There are no human intervention to review before the final output.
>**WARNING**: DO NOT FULLY RELY ON THIS APPLICATION'S CONCEPT IF SYSTEM IS CRITICAL

**Limitation 3:** Step Budget Restrictions<br>
To prevent infinite looping of the agent thinking and planning, step budgets are defined, but could lead to incomplete paraphrasing.
>**Mitigation**: Any instance that went out-of-budget will result in default rephrased sentence - '*Message is offensive*'

**Limitation 4:** Violations Based on Severity<br>
If a chat session contains more than 1 kind of offense, the AI is tasked to provide the more serious offense as the output.
>**If necessary**: Modify the prompt and code if require to list down all the offenses instead

## LLM Models Used (Default Settings)

| Provider | Model(s) | Purpose |
|----------|----------|---------|
| Laya AI | convaiinnovations/laya | Determine if the message is offensive |
| Groq | openai/gpt-oss-20b | LLM used to determine next course of action in an Agentic AI system |
| Ollama (local) | gemma3:4b | LLM that rephrases to non-offensive message |
| Ollama (local) | qwen3 | LLM that determines the policies violated by player |

## Architecture
The following is a simple diagram of the application's architecture:<br><br>
![Architecture Diagram](README_assets/archi.png)