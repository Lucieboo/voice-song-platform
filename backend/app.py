from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "Backend running"}

@app.route("/api/test")
def test():
    return {"status": "API working"}

if __name__ == "__main__":
    app.run()