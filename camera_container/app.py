import time
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, abort, send_file

DATA_DIR = Path("data")
MOCK_DIR = DATA_DIR / "mock"

app = Flask(__name__)
lock = Lock()

def get_json_file_path(month, day=None):
    file_path = MOCK_DIR / f"month_{month}"

    if day:
        filepath = filepath / f"day_{day}.json"

    return file_path.with_suffix("json")

@app.route("/month/<int:month>", methods=["GET"])
def get_month_data(month: int):
    with lock:
        time.sleep(10)

        if month < 1 or month > 12:
            abort(400, description="Bad Request")

        file_path = get_json_file_path(month)

        if not file_path.exists():
            abort(404, description="File not found")
        
        return send_file(file_path, mimetype="application/json")

@app.route("/month/<int:month>/day/<int:day>", methods=["GET"])
def get_day_data(month: int, day: int):
    with lock:
        time.sleep(10)

        if month < 1 or month > 12 or day < 1 or day > 31:
            abort(400, description="Bad Request")

        file_path = get_json_file_path(month, day)

        if not file_path.exists():
            abort(404, description="File not found")

        return send_file(file_path, mimetype="application/json")

@app.errorhandler(404)
def not_found(error):
    response = jsonify({
        "error": "Not Found",
        "message": error.description
    })

    response.status_code = 404

    return response


if __name__ == "__main__":
    app.run(debug=True)
