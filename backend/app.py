from flask import Flask, request, send_file
from flask_cors import CORS
from gtts import gTTS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return {"message": "Backend running"}

@app.route("/generate-voice", methods=["POST"])
def generate_voice():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return {"error": "No text provided"}, 400

    filename = "voice.mp3"

    tts = gTTS(text)
    tts.save(filename)

    return send_file(filename, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)