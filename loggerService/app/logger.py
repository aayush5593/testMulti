from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_data():
    data = request.get_json()
    timestamp = datetime.datetime.now().isoformat()
    log_line = f"[{timestamp}] {data}\n"
    
    # Save to file
    with open("logs.txt", "a") as log_file:
        log_file.write(log_line)
    
    return jsonify({"status": "logged", "data": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
