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
PORT = 18080

@app.route('/check')
def check():
    output = []

    mq = {'_pred': {'$exists':1}}
    num_points = events_in.find(mq).count()
    output.append("Number of data points: {0}".format(num_points))

    mq = {'_pred': "['True']" }
    num_pred_fraud = events_in.find(mq).count()
    output.append("Number predicted fraud: {0}".format(num_pred_fraud))

    mq = {'_pred': "['False']"}
    num_pred_valid = events_in.find(mq).count()
    output.append("Number predicted valid: {0}".format(num_pred_valid))


    """if data and timestamps:
        dt = datetime.fromtimestamp(timestamps[-1])
        data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        line2 = "Latest datapoint received at: {0}".format(data_time)
        line3 = data[-1]
        output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
    else:
        output = line1
    """

    output = '\n'.join(output)
    return output, 200, {'Content-Type': 'text/css; charset=utf-8'}


def register_subscription(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)


if __name__ == '__main__':
    # Register for service subscription
    #ip_address = socket.gethostbyname(socket.gethostname())
    ip_address = "10.5.20.159"

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
