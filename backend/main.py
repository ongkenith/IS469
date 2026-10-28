import sys
from flask import Flask, request, jsonify
from backend.SanitiseProgram import sanitise_program

app = Flask(__name__)

# Configuration Variables
REMOVE_LLM_THINKING_PRINT_STATEMENTS = False

@app.route("/sanitise", methods=["POST"])
def sanitise():
    """
    Sanitise a sentence.

    Expected JSON body:
    {
        "sentence": "Your sentence here",
    }
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    sentence = data.get("sentence", "")

    if not isinstance(sentence, str) or sentence.strip() == "":
        return jsonify({"error": "'sentence' is required and cannot be empty."}), 400

    try:
        result = sanitise_program(
            sentence
        )
    except Exception as exc:
        return jsonify({"error": "Sanitisation failed.", "details": str(exc)}), 500

    return jsonify({
        "input": sentence,
        "result": result
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)