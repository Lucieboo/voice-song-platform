from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import requests
import os

app = Flask(__name__)

# ✅ CORS
CORS(app)

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

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data.get("text")

    try:
        filename = "voice.mp3"
        tts = gTTS(text)
        tts.save(filename)

        return send_file(filename, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🎶 SONG GENERATOR
@app.route("/generate-song", methods=["POST", "OPTIONS"])
def generate_song():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()

    if not data or "lyrics" not in data:
        return jsonify({"error": "No lyrics provided"}), 400

    lyrics = data.get("lyrics")

    try:
        HF_TOKEN = os.getenv("HF_TOKEN")

        if not HF_TOKEN:
            return jsonify({"error": "Missing HuggingFace token"}), 500

        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/musicgen-small",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": lyrics},
            timeout=60
        )

        print("STATUS:", response.status_code)

        # ❌ If AI fails → fallback to voice (VERY IMPORTANT)
        if response.status_code != 200:
            print("FALLBACK TO VOICE")

            tts = gTTS(lyrics)
            tts.save("song.mp3")

            return send_file("song.mp3", mimetype="audio/mpeg")

        # ✅ Save AI audio
        with open("song.wav", "wb") as f:
            f.write(response.content)

        return send_file("song.wav", mimetype="audio/wav")

    except Exception as e:
        print("ERROR:", str(e))

        # 🔥 FINAL fallback (never crash)
        tts = gTTS(lyrics)
        tts.save("song.mp3")

        return send_file("song.mp3", mimetype="audio/mpeg")


# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)