from flask import Flask, request, jsonify
from llm_modules.LayaLLM import LayaLLM
from llm_modules.RephraseAgent import RephraseAgent
from llm_modules.VerdictLLM import VerdictLLM

app = Flask(__name__)
_MODEL = LayaLLM()  # Loaded once, only when you start this server
_REPHRASEAGENT = RephraseAgent()
_VERDICT = VerdictLLM()


@app.route("/laya_predict", methods=["POST"])
def laya_predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not isinstance(data.get("sentence"), str):
        return jsonify({"error": "'sentence' must be a string."}), 400

    return jsonify(_MODEL.is_message_offensive(data["sentence"])), 200

@app.route("/agent_sanitise", methods=["POST"])
def agent_sanitise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not isinstance(data.get("sentence"), str):
        return jsonify({"error": "'sentence' must be a string."}), 400

    return jsonify(_REPHRASEAGENT.start_program(data.get("sentence"))), 200

@app.route("/llm_verdict", methods=["POST"])
def llm_verdict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not isinstance(data.get("chat_history"), str):
        return jsonify({"error": "'chat_history' must be a string."}), 400

    return jsonify(_VERDICT.get_verdict(data["chat_history"])), 200


if __name__ == "__main__":
    # No reloader: this process should stay alive and keep the model in memory.
    # threaded=False is a safe default in case the model isn't thread-safe.
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False, threaded=False)