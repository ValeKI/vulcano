import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from routes.auth import auth_bp
from routes.file import file_bp
from routes.chat import chat_bp
from config import CURRENT_CONFIG

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=[CURRENT_CONFIG.FRONTEND_BASE_URL])

with open("swagger.json", "r", encoding="utf-8") as f:
    swagger_template = json.load(f)

swagger = Swagger(app, template=swagger_template)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(file_bp, url_prefix="/files")
app.register_blueprint(chat_bp, url_prefix="/chat")

if __name__ == "__main__":
    app.run(debug=True)
