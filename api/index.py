from flask import Flask, render_template, request, jsonify
import serial
import time

app = Flask(__name__, template_folder="../templates")

# ✅ Update with your correct port and baudrate
PORT = "COM3"        # Windows example, use "/dev/ttyUSB0" or "/dev/ttyACM0" on Linux
BAUDRATE = 9600

ser = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/connect", methods=["POST"])
def connect():
    global ser
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        time.sleep(2)  # wait for device reset
        return jsonify({"status": "success", "message": f"Connected to {PORT}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/send", methods=["POST"])
def send():
    global ser
    if ser is None or not ser.is_open:
        return jsonify({"status": "error", "message": "Serial port not connected"})
    
    try:
        data = request.json.get("command", "")
        ser.write((data + "\n").encode("utf-8"))
        time.sleep(0.5)
        response = ser.readline().decode("utf-8", errors="ignore").strip()
        return jsonify({"status": "success", "sent": data, "response": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/disconnect", methods=["POST"])
def disconnect():
    global ser
    try:
        if ser and ser.is_open:
            ser.close()
        return jsonify({"status": "success", "message": "Disconnected"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
