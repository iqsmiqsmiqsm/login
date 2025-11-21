from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route("/log", methods=["POST"])
def log():
    data = request.get_data(as_text=True)
    with open("logs.txt", "a") as f:
        f.write(f"\n[{datetime.datetime.now()}]\n{data}\n")
    return "ok"

app.run(host="0.0.0.0", port=9000)
