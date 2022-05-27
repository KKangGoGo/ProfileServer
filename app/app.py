from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello'


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)