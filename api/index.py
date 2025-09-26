from flask import Flask, request, jsonify, make_response, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save_config", methods=["POST"])
def save_config():
    data = request.json
    resp = make_response(jsonify({"status": "✅ Config saved", "config": data}))
    # store each config key in cookies
    for key, value in data.items():
        resp.set_cookie(key, str(value), max_age=60*60*24*7)  # 7 days
    return resp

@app.route("/get_config", methods=["GET"])
def get_config():
    config = {
        "baudRate": request.cookies.get("baudRate"),
        "port": request.cookies.get("port")
    }
    return jsonify(config)

@app.route("/send_command", methods=["POST"])
def send_command():
    data = request.json
    cmd = data.get("command")
    baud = request.cookies.get("baudRate")
    port = request.cookies.get("port")

    # Just log for now
    print(f"📤 Command: {cmd}, Using Config: baud={baud}, port={port}")
    return jsonify({"status": "✅ Command sent", "command": cmd, "config": {"baudRate": baud, "port": port}})

if __name__ == "__main__":
    app.run(debug=True)
