from flask import Flask, request, jsonify
from flask_cors import CORS
from PredictProgram import predict_program
from SanitiseProgram import sanitise_program
from VerdictProgram import get_verdict

app = Flask(__name__)
CORS(app)


@app.route("/predict", methods=["POST"])
def predict():
    """ Check if a sentence is offensive. If yes, sanitise it """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    sentence = data.get("sentence", "")["text"]

    if not isinstance(sentence, str) or sentence.strip() == "":
        return jsonify({"error": "'sentence' is required and cannot be empty."}), 400

    try:
        result = predict_program(sentence)

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
        return jsonify({"error": "Prediction failed.", "details": str(exc)}), 500


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
        pass
        result = sanitise_program(
            sentence
        )

        if result[1] == 0:  # IF no error
            return jsonify({
                "input": sentence,
                "message": f"*{result[0]}*"
            }), 200
        elif result[1] == -1:
            return jsonify({
                "input": sentence,
                "message": "*Message is offensive*"
            }), 200
        
    except Exception as exc:
        print(f"[Error] {exc}")
        return jsonify({"error": "Sanitisation failed.", "details": str(exc)}), 500


@app.route("/gives_verdict", methods=["POST"])
def gives_verdict():
    """ Given that the chat contains offensive messages, provide verdict """
    data = request.get_json(silent=True)
    
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    sentences = data.get("sentences", [])

    if not isinstance(sentences, list) or len(sentences) == 0:
        return jsonify({"error": "'sentence' is required and cannot be empty."}), 400

    try:
        print("[Action] Calling LLM to determine violations hit")
        chat_history = " ".join(sentences)
        final_verdict = get_verdict(chat_history)

        if final_verdict[1] == 0:
            return jsonify({
                "message": final_verdict[0]
            }), 200
        else:
            return jsonify({
                "message": ""
            }), 200

    except Exception as exc:
        return jsonify({"error": "Verdict failed.", "details": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)