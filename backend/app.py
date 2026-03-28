from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import requests
import os

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


# 🔐 TEMP USER STORAGE
users = {}

@app.route("/")
def home():
    return jsonify({"message": "AI Studio Backend Running"})


# =========================
# 🔐 AUTH ROUTES
# =========================

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return jsonify({"error": "User already exists"}), 400

    users[email] = password
    return jsonify({"message": "Signup successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if users.get(email) != password:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"})


# =========================
# 🎤 VOICE
# =========================
@app.route("/generate-voice", methods=["POST", "OPTIONS"])
def generate_voice():
    if request.method == "OPTIONS":
        return "", 200

    text = request.json.get("text")

    tts = gTTS(text)
    tts.save("voice.mp3")

    return send_file("voice.mp3", mimetype="audio/mpeg")


# =========================
# 🎶 SONG
# =========================
@app.route("/generate-song", methods=["POST", "OPTIONS"])
def generate_song():
    if request.method == "OPTIONS":
        return "", 200

    lyrics = request.json.get("lyrics")

    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/musicgen-small",
        headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"},
        json={"inputs": lyrics}
    )

    with open("song.wav", "wb") as f:
        f.write(response.content)

    return send_file("song.wav", mimetype="audio/wav")


# =========================
# 🖼️ IMAGE
# =========================
@app.route("/generate-image", methods=["POST", "OPTIONS"])
def generate_image():
    if request.method == "OPTIONS":
        return "", 200

    prompt = request.json.get("prompt")

    response = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"},
        json={"inputs": prompt}
    )

    with open("image.png", "wb") as f:
        f.write(response.content)

    return send_file("image.png", mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)