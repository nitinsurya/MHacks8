#!flask/bin/python


from flask import Flask, request, send_from_directory, jsonify, make_response, abort
import os
import requests

app = Flask(__name__, static_url_path='')

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
    json_data = req.json()
    out_vals = {'curr_bal': {'val': str(10000 - json_data['balance']), 'text-sub': "Due on Nov 6"},
        'credit': {'val': str(json_data['balance']), 'text-sub': "Credit limit: $10000"}}
    url = "http://api.reimaginebanking.com/accounts/" + account_id + "/purchases?key=" + mhack_key
    req = requests.get(url)
    json_data = req.json()
    for elem in json_data:
      merchant_details = merchant_data[elem['merchant_id']]
      if coords:
        out_vals['transactions'] = [{'name': merchant_details['name'], 'date': get_format_data(elem['purchase_date']), 'amount': str(elem['amount']),
                  'lat': merchant_details['lat'], 'lon': merchant_details['lng']},
                {'name': 'Chapati Indian Grill', 'date': 'SATURDAY, OCT 8', 'amount': "$44.05", 'lat': "41.879483", 'lon': "-88.0998467"}]
      else:
        out_vals['transactions'] = [{'name': merchant_details['name'], 'date': get_format_data(elem['purchase_date']), 'amount': str(elem['amount'])},
                            {'name': 'Chapati Indian Grill', 'date': 'SATURDAY, OCT 8', 'amount': "$44.05"}]
  else:
    out_vals = {"error": "Something went wrong"}

  out_vals['subscriptions'] = [{'name': 'Spotify', 'date': 'Scheduled on Oct 8', 'amount': "$9.99"},
                        {'name': 'Google Express', 'date': 'Scheduled on Oct 14', 'amount': "$10.00"},
                        {'name': 'LinkedIn Subscription', 'date': 'Scheduled on Oct 16', 'amount': "$29.99"}]
  return make_response(jsonify(out_vals))

@app.route('/app_events', methods=['GET'])
def app_events():
  out_vals = [{
                "title": "event1",
                "start": "2016-10-20"
              }, {
                "title": "event2",
                "start": "2016-10-05",
                "end": "2016-10-07"
              }, {
                "title": "event3",
                "start": "2016-10-09T12:30:00",
                "allDay": False
              }]
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


def get_format_data(date_str):
  return date_str

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8081, debug=True, threaded=True)
