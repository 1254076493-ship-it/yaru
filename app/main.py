from flask import Flask, render_template, request, jsonify
from generator import generate_copy

app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    data = request.get_json(silent=True) or {}
    keywords = (data.get("keywords") or "").strip()
    if not keywords:
        return jsonify({"error": "请输入关键词"}), 400

    content = generate_copy(keywords, signature="XX")
    return jsonify({"content": content})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
