from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime
from pymongo import MongoClient
import pymongo

mcl = MongoClient()
mdb = mcl['events']
events_in = mdb['incoming']

app = Flask(__name__)
PORT = 18080

@app.route('/check')
def check():
    output = []

    output.append("<html><head>")
    output.append("<title>Real-Time Predictions</title>")
    output.append("</head>")
    output.append("<body style='font-family:sans-serif; background-color: black; color: white'>")

    output.append("<h1 style='color:#ff88aa'>Fraud Dashboard</h1>")
    output.append("<h2 style='color:#ff88aa'>Summary</h2>")
    output.append("<ul>")
    mq = {'_pred': {'$exists':1}}
    num_points = events_in.find(mq).count()
    output.append("<li style='color:#88ffaa'>Number of data points: {0}</li>".format(num_points))

    mq = {'_pred': "['True']" }
    num_pred_fraud = events_in.find(mq).count()
    output.append("<li style='color:#88ffaa'>Number predicted fraud: {0}</li>".format(num_pred_fraud))

    mq = {'_pred': "['False']"}
    num_pred_valid = events_in.find(mq).count()
    output.append("<li style='color:#88ffaa'>Number predicted valid: {0}</li>".format(num_pred_valid))
    output.append("</ul>")

    output.append("<h2 style='color:#ff88aa'>Newest Flagged Events</h2>")
    output.append("<table style='border-collapse: collapse; border: 1px solid grey'; background-color: #330000>")
    output.append("<tr><th style='border: 1px solid grey'>Title</th><th style='border: 1px solid grey'>Probability</th></tr>")

    # List potentially fraudulent events
    mq = {'_pred': "['True']" }
    fraud_events = num_pred_fraud = events_in.find(mq).sort('_id', pymongo.DESCENDING)

    for event in fraud_events:
        s = "<tr><td style='border: 1px solid grey'>"
        s += event['name']
        s += "</td><td style='border: 1px solid grey; color:red'>"
        s += event['_prob'][1:5]
        s += "</td></tr>"
        output.append(s)

    output.append('</table></body></html>')

    output = '\n'.join(output)
    return output, 200, {'Content-Type': 'text/html; charset=utf-8'}



if __name__ == '__main__':
    # Register for service subscription
    #ip_address = socket.gethostbyname(socket.gethostname())
    ip_address = "10.5.20.159"

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
