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

    output.append("<h1>Fraud Dashboard</h1>")
    output.append("<h2>Summary</h2>")
    output.append("<ul>")
    mq = {'_pred': {'$exists':1}}
    num_points = events_in.find(mq).count()
    output.append("<li>Number of data points: {0}</li>".format(num_points))

    mq = {'_pred': "['True']" }
    num_pred_fraud = events_in.find(mq).count()
    output.append("<li>Number predicted fraud: {0}</li>".format(num_pred_fraud))

    mq = {'_pred': "['False']"}
    num_pred_valid = events_in.find(mq).count()
    output.append("<li>Number predicted valid: {0}</li>".format(num_pred_valid))
    output.append("</ul>")

    output.append("<h2>Newest Flagged Events</h2>")
    output.append("<table style='border-collapse: collapse'")
    output.append("<tr><th style='background-color:#225; color:#ccc'>Title</th><th style='background-color:#225; color:#ccc'>Probability</th></tr>")

    # List potentially fraudulent events
    mq = {'_pred': "['True']" }
    fraud_events = num_pred_fraud = events_in.find(mq).sort('_id', pymongo.DESCENDING)

    for event in fraud_events:
        s = "<tr><td style='background-color:#ccc; color:#500; border: 1px solid grey'>"
        s += event['name']
        s += "</td><td style='background-color:#ccc; border: 1px solid grey; color:#500'>"
        s += event['_prob'][1:5]
        s += "</td></tr>"
        output.append(s)

    output.append('</table></body></html>')

    output = '\n'.join(output)
    return output, 200, {'Content-Type': 'text/html; charset=utf-8'}



if __name__ == '__main__':
    # Register for service subscription
    #ip_address = socket.gethostbyname(socket.gethostname())
    ip_address = "10.5.20.159"  #TODO remove hardcoded IP address

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
