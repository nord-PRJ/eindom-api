#!flask/bin/python
from flask import Flask, jsonify, make_response, send_from_directory, g
import csv, sqlite3

app = Flask(__name__)

DATABASE = ':memory:'

@app.route('/')
def index():
    return "Eindom API"

# TODO make functionality to add CSV to DB
@app.route('/csv/date/<file_name>', methods=['POST'])
def add_csv_to_db(file_name):
    cur = get_db().cursor()
    with open('./finnestate-crawl/finnestate/data/' + file_name + '.csv', 'rt') as fin:
    # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [(i['price'], i['ad_title'], i['href'], i['rooms'], i['owner'], i['real_estate_firm'], i['id'], i['common_expenses'], i['common_debt'], i['img_href'], i['building_type'], i['location'], i['square_meter']) for i in dr]
    cur.execute('''CREATE TABLE IF NOT EXISTS finn_bredth_search ( price, ad_title, href, rooms, owner, real_estate_firm, id, common_expenses, common_debt, img_href, building_type, location, square_meter);''')
    cur.executemany("INSERT INTO finn_bredth_search ( price, ad_title, href, rooms, owner, real_estate_firm, id, common_expenses, common_debt, img_href, building_type, location, square_meter) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    return jsonify({'Entry': "Created"}), 201

# TODO make functionality to return CSV from DB
@app.route('/csv/date/<file_name>', methods=['GET'])
def get_csv_by_date(file_name):
    return send_from_directory('./finnestate-crawl/finnestate/data/', file_name + '.csv', as_attachment=True)

@app.route('/getall', methods=['GET'])
def get_all():
    cur = get_db().cursor()
    data = cur.execute("SELECT * FROM finn_bredth_search")
    return jsonify(list(data))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
