import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from SanitiseProgram import sanitise_program
from classes.LayaClient import LayaClient

app = Flask(__name__)
CORS(app)


@app.route("/sanitise", methods=["POST"])
def sanitise():
    """ Check if a sentence is offensive. If yes, sanitise it """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    sentence = data.get("sentence", "")["text"]

    if not isinstance(sentence, str) or sentence.strip() == "":
        return jsonify({"error": "'sentence' is required and cannot be empty."}), 400

    try:
        result = sanitise_program(
            sentence,
            loaded_model = _LAYAMODEL
        )

        if result[1] == 0:  # IF found not offensive
            return jsonify({
                "input": sentence,
                "message": result[0]
            }), 200
        elif result[1] == 1:  # If found offensive
            return jsonify({
                "input": sentence,
                "message": "[To be rewritten]"
            }), 200
        elif result[1] == -1:
            return jsonify({
                "input": sentence,
                "message": result[0]
            }), 200
        
    except Exception as exc:
        print(f"[Error] {exc}")
        return jsonify({"error": "Sanitisation failed.", "details": str(exc)}), 500

@app.route("/summarise_chat_history", methods=["POST"])
def summarise_chat_history():
    """ Check if a chat history is offensive. If yes, provide customised warning message """
    data = request.get_json(silent=True)
    
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    sentences = data.get("sentences", [])

    if not isinstance(sentences, list) or len(sentences) == 0:
        return jsonify({"error": "'sentence' is required and cannot be empty."}), 400

    try:
        print("[Action] Calling Agent to see if chat history is to give warning")
    except Exception as exc:
        return jsonify({"error": "Sanitisation failed.", "details": str(exc)}), 500

    return jsonify({
        "message": "TO BE DETERMINED"
    }), 200


if __name__ == "__main__":
    # Load any LLM model that will be used before Flask App begins
    _LAYAMODEL = LayaClient()

    app.run(host="0.0.0.0", port=5000, debug=True)