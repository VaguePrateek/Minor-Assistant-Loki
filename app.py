from flask import Flask, jsonify, render_template, request
from loki_core import handle_command

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}
    command = (data.get("command") or "").strip()
    if not command:
        return jsonify({"responses": ["Please say or type a command."], "url": None}), 400
    return jsonify(handle_command(command))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
