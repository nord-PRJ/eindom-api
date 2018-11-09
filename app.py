#!flask/bin/python
from flask import Flask, jsonify, make_response, send_from_directory
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return "Eindom API"

# TODO make functionality to return CSV from DB


@app.route('/csv/date/<filename>', methods=['GET'])
def get_csv_by_date(filename):
    file_name = request.view_args['filename']
    return send_from_directory('/finnestate-crawl/finnestate/data/', file_name + '.csv', as_attachment=True)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
