from flask import Flask, request, jsonify
from flask_cors import CORS
from mock.db_mock import USERS
from commands.login_command import LoginCommand

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<h1>Hello World! Vulcano!</h1>"

@app.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        cmd = LoginCommand.from_dict(data)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400

    # Controllo credenziali mock
    if USERS.get(cmd.usernameOrEmail) == cmd.password:
        return jsonify({
            "token": "mock-jwt-token-123456",
            "user": {"usernameOrEmail": cmd.usernameOrEmail}
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/auth/check", methods=["GET"])
def check():
    try:
        data = request.get_json()
        cmd = data.get("token")
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)