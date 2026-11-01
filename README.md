# IS469 Project: Offensive Message Detection & Rephrasing
Using Large Language Models (LLMs) to detect offensive messages and suggest respectful rephrasings that preserve the sender's original intent.

### Overview ###
This project explores how non-autoregressive System 1 decision model can be used to flag offensive or toxic messages, and use LLMs to automatically rewrite them in a more constructive tone while maintaining the message, instead of relying on pattern matching like Regex and mask messages with asterisk. <br>

## Demo
Users submit a message, the system classifies whether it is offensive, and, if so, returns a rephrased version.
<To add the pictures>

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
3. **Pull the following Ollama models**
```bash
ollama pull <model-name>
```
4. **Set up environment variables**<br>
Make a copy of .env.example file under 'model_server' folder and add your GROQ API key

### Running the Application

Start each service in a separate terminal:

```bash
# Terminal 1: Model Server
cd model_server
python model_server.py

# Terminal 2: Backend
cd backend
python main.py

# Terminal 3: Frontend
cd frontend
npm run dev
```
The app will be available at `http://localhost:3000`

## Limitations of Applications

## LLM Models Used

| Provider | Model(s) | Purpose |
|----------|----------|---------|
| Laya AI | convaiinnovations/laya | Determine if the message is offensive |
| Groq | openai/gpt-oss-20b | LLM used to determine next course of action in an Agentic AI system |
| Ollama (local) | --To be confirmed-- | LLM that rephrases to non-offensive message |

## Architecture