from flask import Flask,  request, jsonify

app = Flask(__name__)

X_QA_SECRET_TOKEN="secret-token"

@app.before_request
def verify_qa_token():
    token = request.headers.get("X-QA-Secret-Token")

    if token != X_QA_SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401


@app.route("/calls/log", methods=["POST"])
def call_log():
    required_fields = ["name"]
    data = request.get_json()

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing {field}"})
    
    for field in data:
        if field not in required_fields:
            return jsonify({"error": "Invalid data"})

    return request.get_json()
