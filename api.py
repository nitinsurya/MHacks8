#!flask/bin/python


from flask import Flask, request, send_from_directory, jsonify, make_response, abort
import os
import requests
from flask_cors import CORS, cross_origin
from collections import Counter
import datetime

app = Flask(__name__, static_url_path='')
CORS(app)

mhack_key = "cb3e8a83305f920c21ee1b74e7694bcf"

merchant_data = {
  '57f8c214360f81f104543be0': {
    "name": "Chapathi",
    "city": "Chicago",
    "state": "IL",
    "lat": 41.879483,
    "lng": -88.0998467,
    "category": [
      "Food"
    ]
  },
  '57cf75cea73e494d8675ec4f': {
    "name": "Zimet Musical Services",
    "city": "Ithaca",
    "state": "NY",
    "lat": 42.4497493,
    "lng": -76.50136429999999,
    "category": [
      "store",
      "point_of_interest",
      "establishment"
    ]
  },
  '57cf75cea73e494d8675ed1f': {
    "name": "Verizon Authorized Retailer - Cellular Sales",
    "lat": 40.391877,
    "lng": -86.8514601,
    "city": "Lafayette",
    "state": "IN",
    "category": [
      "store",
      "point_of_interest",
      "establishment"
    ]
  },
  '57cf75cea73e494d8675ed1c': {
    "name": "Triple XXX Family Restaurant",
    "lat": 40.42272849999999,
    "lng": -86.9054049,
    "city": "West Lafayette",
    "street number": "2",
    "state": "IN",
    "category": [
      "restaurant",
      "food",
      "point_of_interest",
      "establishment"
    ]
  },
  '57cf75cea73e494d8675ed23': {
    "name": "Papa John's Pizza",
    "category": [
      "meal_delivery",
      "meal_takeaway",
      "restaurant",
      "food",
      "point_of_interest",
      "establishment"
    ],
    "lat": 40.4334587,
    "lng": -86.8693725,
    "city": "Lafayette",
    "state": "IN",
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
    pie_data = []
    
    if coords:
      out_vals = {'curr_bal': {'val': str(round(10000 - json_data1['balance'], 2)), 'text-sub': "Nov 6"},
        'credit': {'val': str(json_data1['balance']), 'text-sub': "$10000"}, 'transactions': []}
      for elem in json_data:
        merchant_details = merchant_data[elem['merchant_id']]
        pie_data.append(merchant_details['category'])
        out_vals['transactions'].append({'name': merchant_details['name'],
                          'date': get_format_date(datetime.datetime.strptime(elem['purchase_date'], "%Y-%m-%d").date()),
                          'amount': str(elem['amount']),
                          'lat': merchant_details['lat'], 'lon': merchant_details['lng']})
    else:
      out_vals = {'curr_bal': {'val': round(10000 - json_data1['balance'], 2), 'text-sub': "Due on Nov 6"},
        'credit': {'val': str(json_data1['balance']), 'text-sub': "Credit limit: $10000"}, 'transactions': []}
      for elem in json_data:
        merchant_details = merchant_data[elem['merchant_id']]
        pie_data.append(merchant_details['category'])
        out_vals['transactions'].append({'name': merchant_details['name'],
          'date': get_format_date(datetime.datetime.strptime(elem['purchase_date'], "%Y-%m-%d").date()), 'amount': str(elem['amount'])})
  else:
    return make_response(jsonify({"error": "Something went wrong"}))

  url = "http://api.reimaginebanking.com/accounts/" + account_id + "/bills?key=" + mhack_key
  req = requests.get(url).json()
  out_vals['subscriptions'] = get_subscription_data(True)
  out_vals['pie_content'] = get_pie_content(pie_data)
  return make_response(jsonify(out_vals))

@app.route('/app_events', methods=['GET'])
def app_events():
  account_id, out_vals = '57f89267360f81f104543bd1', []
  url = "http://api.reimaginebanking.com/accounts/" + account_id + "/purchases?key=" + mhack_key
  json_data = requests.get(url).json()
  
  for elem in json_data:
    out_vals.append({"title": merchant_data[elem['merchant_id']]['name'] + "\n$" + str(elem['amount']), "start": elem['purchase_date'], "color": "blue"})

  for elem in get_subscription_data():
    out_vals.append({"title": elem['name'] + "\n" + elem['amount'], 'start': elem['start_date'], "color": "red"})

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

def get_subscription_data(scheduled = False):
  account_id, out_vals = '57f89267360f81f104543bd1', []
  url = "http://api.reimaginebanking.com/accounts/" + account_id + "/bills?key=" + mhack_key
  json_data = requests.get(url).json()
  for elem in json_data:
    date_formatted = get_format_date(datetime.datetime.strptime(elem['payment_date'], "%Y-%m-%d").date())
    out_vals.append({'name': elem['payee'], 'start_date': elem['payment_date'],
      'date': "Scheduled on " + date_formatted if scheduled else date_formatted,
      'amount': '$' + str(elem['payment_amount'])})

  return out_vals

def get_format_date(date_str):
  return date_str.strftime('%d, %b %Y')

def get_pie_content(data):
  out_val, tmp_val = [['category', 'amount']], [] 

  for elem in data:
    tmp_val = tmp_val + [el.lower() for el in elem]
  tmp_val = Counter(tmp_val).most_common(5)
  for key in tmp_val:
    out_val.append([key[0].replace("_", " ").capitalize(), key[1]])
  return out_val

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8081, debug=True, threaded=True)
