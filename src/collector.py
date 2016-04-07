from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime
from pymongo import MongoClient
import clean_data_code
import graphlab as gl

mcl = MongoClient()
mdb = mcl['events']
events_in = mdb['incoming']

app = Flask(__name__)
PORT = 5353
REGISTER_URL = "http://10.5.81.89:5000/register"


def predict_fraud(json_input):
    """Add fraud probability to json input"""
    df = clean_data_code.mongo_to_df(json_input)
    abt = clean_data_code.transform_df(df)
    model = gl.load_model('../models/btc_priceless_v1.gl')
    sf = gl.SFrame(abt)
    pred = model.predict(sf)
    prob = model.predict(sf, output_type='probability')

    ev = json_input.copy()
    ev['_pred'] = str(pred)
    ev['_prob'] = str(prob)
    return ev


@app.route('/score', methods=['POST'])
def score():

    this_event = request.json
    #event_time = time.time()
    ev = predict_fraud(this_event)
    events_in.insert_one(ev)

    return ""


def register_subscription(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)


if __name__ == '__main__':
    # Register for service subscription
    #ip_address = socket.gethostbyname(socket.gethostname())
    ip_address = "10.5.20.159"
    print "attempting to register %s:%d" % (ip_address, PORT)
    register_subscription(ip_address, str(PORT))

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
