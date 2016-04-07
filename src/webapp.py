from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime
from pymongo import MongoClient

mcl = MongoClient()
mdb = mcl['events']
events_in = mdb['incoming']

app = Flask(__name__)
PORT = 5353
REGISTER_URL = "http://10.5.81.89:5000/register"

data = []
timestamps= []


@app.route('/score', methods=['POST'])
def score():

    this_event = request.json
    #event_time = time.time()

    events_in.insert_one(this_event)

    return ""


@app.route('/check')
def check():
    line1 = "Number of data points: {0}".format(len(data))
    if data and timestamps:
        dt = datetime.fromtimestamp(timestamps[-1])
        data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        line2 = "Latest datapoint received at: {0}".format(data_time)
        line3 = data[-1]
        output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
    else:
        output = line1
    return output, 200, {'Content-Type': 'text/css; charset=utf-8'}


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
