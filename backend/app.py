from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import requests
import os

app = Flask(__name__)

# ✅ CORS FIX (VERY IMPORTANT)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


@app.route("/")
def home():
    return jsonify({"message": "AI Voice + Song Backend Running"})


# 🎤 TEXT TO SPEECH
@app.route("/generate-voice", methods=["POST", "OPTIONS"])
def generate_voice():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = "voice.mp3"

    tts = gTTS(text)
    tts.save(filename)

    return send_file(filename, mimetype="audio/mpeg")


# 🎶 SONG GENERATOR
@app.route("/generate-song", methods=["POST", "OPTIONS"])
def generate_song():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    lyrics = data.get("lyrics")

    if not lyrics:
        return jsonify({"error": "No lyrics provided"}), 400

    # 🔥 IMPROVED PROMPT
    prompt = f"Generate a musical song with instruments. {lyrics}"

    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/musicgen-small",
        headers={
            "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
        },
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        return jsonify({"error": response.text}), 500

    with open("song.wav", "wb") as f:
        f.write(response.content)

    return send_file("song.wav", mimetype="audio/wav")


# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)