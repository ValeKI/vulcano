from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.file import file_bp
from routes.chat import chat_bp

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:5173"])

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(file_bp, url_prefix="/files")
app.register_blueprint(chat_bp, url_prefix="/chat")

if __name__ == "__main__":
    app.run(debug=True)
