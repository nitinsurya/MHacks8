#!flask/bin/python


from flask import Flask, request, send_from_directory, jsonify, make_response, abort
import os
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='')
CORS(app)

mhack_key = "cb3e8a83305f920c21ee1b74e7694bcf"

merchant_data = {
  '57f8c214360f81f104543be0': {
    "name": "Chapathi",
    "city": "Chicago",
    "state": "IL",
    "lat": 41.879483,
    "lng": -88.0998467
  }
}

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/js/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)

@app.route('/app_content', methods=['GET'])
def app_content():
  coords = request.args.get('coords')
  account_id = '57f89267360f81f104543bd1'
  url = "http://api.reimaginebanking.com/accounts/" + account_id + "?key=" + mhack_key
  req = requests.get(url)
  if req.status_code == 200:

    json_data1 = req.json()
    url = "http://api.reimaginebanking.com/accounts/" + account_id + "/purchases?key=" + mhack_key
    json_data = requests.get(url).json()
    
    for elem in json_data:
      merchant_details = merchant_data[elem['merchant_id']]
      if coords:
        out_vals = {'curr_bal': {'val': str(round(10000 - json_data1['balance'], 2)), 'text-sub': "Nov 6"},
          'credit': {'val': str(json_data1['balance']), 'text-sub': "$10000"}}
        out_vals['transactions'] = [{'name': merchant_details['name'], 'date': get_format_date(elem['purchase_date']), 'amount': str(elem['amount']),
                  'lat': merchant_details['lat'], 'lon': merchant_details['lng']},
                {'name': 'Chapati Indian Grill', 'date': 'SATURDAY, OCT 8', 'amount': "$44.05", 'lat': 41.879483, 'lon': -88.1098467}]
      else:
        out_vals = {'curr_bal': {'val': round(10000 - json_data1['balance'], 2), 'text-sub': "Due on Nov 6"},
          'credit': {'val': str(json_data1['balance']), 'text-sub': "Credit limit: $10000"}}
        out_vals['transactions'] = [{'name': merchant_details['name'], 'date': get_format_date(elem['purchase_date']), 'amount': str(elem['amount'])},
                            {'name': 'Chapati Indian Grill', 'date': 'SATURDAY, OCT 8', 'amount': "$44.05"}]
  else:
    return make_response(jsonify({"error": "Something went wrong"}))

  url = "http://api.reimaginebanking.com/accounts/" + account_id + "/bills?key=" + mhack_key
  req = requests.get(url).json()
  out_vals['subscriptions'] = get_subscription_data()
  out_vals['pie_content'] = get_pie_content()
  return make_response(jsonify(out_vals))

@app.route('/app_events', methods=['GET'])
def app_events():
  account_id, out_vals = '57f89267360f81f104543bd1', []
  url = "http://api.reimaginebanking.com/accounts/" + account_id + "/purchases?key=" + mhack_key
  json_data = requests.get(url).json()
  
  for elem in json_data:
    out_vals.append({"title": merchant_data[elem['merchant_id']]['name'] + " $" + str(elem['amount']), "start": elem['purchase_date'], "color": "blue"})

  for elem in get_subscription_data():
    out_vals.append({"title": elem['name'] + " $" + elem['amount'], 'start': elem['start_date'], "color": "red"})

  return make_response(jsonify(out_vals))

@app.route('/mhacks', methods=['GET'])
def mhacks():
  url = "http://api.reimaginebanking.com/accounts?key=" + mhack_key
  req = requests.get(url)
  if req.status_code == 200:
      out_vals = req.json()
  else:
      out_vals = {"error": "Something went wrong"}
  return make_response(jsonify(out_vals), req.status_code)

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

def get_subscription_data():
  return [{'name': 'Spotify', 'date': 'Scheduled on Oct 8', 'start_date': "2016-10-08", 'amount': "$9.99"},
                        {'name': 'Google Express', 'date': 'Scheduled on Oct 14', 'start_date': "2016-10-14", 'amount': "$10.00"},
                        {'name': 'LinkedIn Subscription', 'date': 'Scheduled on Oct 16', 'start_date': "2016-10-16", 'amount': "$29.99"}]

def get_format_date(date_str):
  return date_str

def get_pie_content():
  return [['category', 'amount'], ['Food', 4], ['Travel', 2], ['Entertainment', 2]]

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8081, debug=True, threaded=True)
