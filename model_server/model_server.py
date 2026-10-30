from flask import Flask, request, jsonify
from classes.LayaClass import LayaLLM

app = Flask(__name__)
_MODEL = LayaLLM()  # Loaded once, only when you start this server


@app.route("/laya_predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not isinstance(data.get("sentence"), str):
        return jsonify({"error": "'sentence' must be a string."}), 400

    return jsonify(_MODEL.is_message_offensive(data["sentence"])), 200


if __name__ == "__main__":
    # No reloader: this process should stay alive and keep the model in memory.
    # threaded=False is a safe default in case the model isn't thread-safe.
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False, threaded=False)