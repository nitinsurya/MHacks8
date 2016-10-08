#!flask/bin/python


from flask import Flask, request, send_from_directory, jsonify, make_response, abort
import os
import requests

app = Flask(__name__, static_url_path='')

mhack_key = "cb3e8a83305f920c21ee1b74e7694bcf"

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/js/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)

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

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8081, debug=True, threaded=True)
