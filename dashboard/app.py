from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os, json, time, threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
LOG = os.path.join("..", "logs", "ml_predictions.log")

@app.route("/")
def index():
    return render_template("index.html")

def stream_log():
    with open(LOG, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            try:
                if line.startswith("ML DECISION: "):
                    payload = json.loads(line.replace("ML DECISION: ", ""))
                    socketio.emit("ml_update", payload)
            except:
                pass

@socketio.on("connect")
def connect():
    emit("status", {"msg": "Connected to RBOTzilla feed"})

if __name__ == "__main__":
    threading.Thread(target=stream_log).start()
    socketio.run(app, host="0.0.0.0", port=8000)
