from flask import Flask, request, jsonify
import datetime
import json
import os

app = Flask(__name__)

LOG_FILE = "logs.txt"

@app.route('/', methods=['GET'])
def home():
    return "Logger service is running", 200

@app.route('/log', methods=['POST'])
def log_data():
    data = request.get_json()
    timestamp = datetime.datetime.now().isoformat()
    log_line = f"[{timestamp}] {json.dumps(data)}\n"

    # Save to file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_line)

    return jsonify({"status": "logged", "data": data}), 200

@app.route('/summary', methods=['GET'])
def summary():
    if not os.path.exists(LOG_FILE):
        return jsonify({"error": "No logs found"}), 404

    stats = {
        "total_requests": 0,
        "operations": {},
        "errors": 0
    }

    with open(LOG_FILE, "r") as log_file:
        for line in log_file:
            try:
                log_json = json.loads(line.split("] ")[1])
                stats["total_requests"] += 1

                if log_json.get("status") == "error":
                    stats["errors"] += 1

                op = log_json.get("operation")
                if op:
                    stats["operations"][op] = stats["operations"].get(op, 0) + 1
            except Exception:
                continue  # Ignore badly formatted lines

    return jsonify(stats), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
