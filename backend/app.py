from flask import Flask, request, send_file
from flask_cors import CORS
from gtts import gTTS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "AI Voice Backend Running"}

@app.route("/generate-voice", methods=["POST"])
def generate_voice():
    text = request.json.get("text")

    tts = gTTS(text)
    filename = "voice.mp3"
    tts.save(filename)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)