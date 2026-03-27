from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return jsonify({"message": "AI Voice + Song Backend Running"})

# 🎤 TEXT TO SPEECH
@app.route("/generate-voice", methods=["POST"])
def generate_voice():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = "voice.mp3"

    tts = gTTS(text)
    tts.save(filename)

    return send_file(filename, mimetype="audio/mpeg")


# 🎶 SONG GENERATION (Hugging Face)
@app.route("/generate-song", methods=["POST"])
def generate_song():
    data = request.get_json()
    lyrics = data.get("lyrics")

    if not lyrics:
        return jsonify({"error": "No lyrics provided"}), 400

    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
    }

    response = requests.post(API_URL, headers=headers, json={
        "inputs": lyrics
    })

    if response.status_code != 200:
        return jsonify({"error": "Song generation failed"}), 500

    with open("song.wav", "wb") as f:
        f.write(response.content)

    return send_file("song.wav", mimetype="audio/wav")


# REQUIRED FOR RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)