import os
from pathlib import Path

from flask import Flask, request, send_file, jsonify

app = Flask(__name__)
current_path = Path(os.path.dirname(os.path.realpath(__file__)))


@app.route('/data')
def get_csv():
    if "date" not in request.args:
        return jsonify({'error': "value for 'date' is missing"}), 400

    try:
        date = str(request.args["date"])
    except (Exception, ):
        return jsonify({'error': "value for 'date' should be a string"}), 400

    csv_dir = f"{current_path}/data"
    csv_file = f"{date}_data.csv"
    csv_path = os.path.join(csv_dir, csv_file)

    if not os.path.isfile(csv_path):
        return jsonify({'error': f"file {csv_file} was not found on the server"}), 400

    return send_file(csv_path, as_attachment=True)


@app.route('/')
def myapp():
    message = f"To use this app: {request.base_url[:-1]}:5000/data?date=YYYYMMDD"
    return message
