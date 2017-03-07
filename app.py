from flask import Flask, request, render_template, send_file, jsonify, session
from flask_triangle import Triangle
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
from flask_uuid import FlaskUUID
from uuid import uuid4
from pymongo import MongoClient
import random as rand
from itertools import product
import json, os
from EpsilonGreedy import EpsilonGreedy
from UCB import UCB

# Create app and PyMongo DB
app = Flask(__name__)
Triangle(app)
socketio = SocketIO(app)
flask_uuid = FlaskUUID()
flask_uuid.init_app(app)

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

# Set app secret (for sessions).
app.secret_key = os.urandom(24)

# Layout features and options
layouts = ["grid", "list"]
font_sizes = ["small", "large"]
colour_schemes = ["dark", "light"]
features = [layouts, font_sizes, colour_schemes]
# Initialise bandit algorithm
bandit = UCB(features)

@app.route("/")
def index():
	session['uid'] = uuid4()
	return render_template('index.html', layout=generate_layout())

@app.route("/registerClick", methods=['POST'])
def registerClick():
	try:
		session['clicks'] += 1
		print 'clicks: ', session['clicks']
		# Update MongoDB entry
		# db.Clicks.update_one({'session_id': session['uid']},{'$set': {'clicks': session['clicks']}}, upsert=False)
		# bandit.updateValue(session['layoutType'], session['clicks'])
		return jsonify(status='OK',message='Incremented clicks successfully')

	except Exception,e:
		return jsonify(status='ERROR',message=str(e))

@app.route("/registerTime", methods=['POST'])
def registerTime():
	# try:
	json_data = request.json['time']
	session['time'] = convert_to_seconds(json_data)
	print 'clicks: ', session['clicks']
	reward = {'clicks': session['clicks'], 'time': session['time']}
	print reward
	# Update MongoDB entry
	bandit.updateValue(session['layoutType'], reward)
	# db.Clicks.update_one({'session_id': session['uid']},{'$set': {'time': session['time']}}, upsert=False)
	# bandit.updateValue(session['layoutType'], session['clicks'])
	return jsonify(status='OK',message='Incremented clicks successfully')

	# except Exception,e:
	# 	return jsonify(status='ERROR',message=str(e))

# DASHBOARD functions
@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html')

def generate_layout():
	# get all feature combinations
	versions = list(product(features[0], features[1], features[2]))
	print "clicks db: ", db.Clicks.count()
	if db.Clicks.count() == 0:
		for v in versions:
			print v
			db.Clicks.insert_one({'layout': v[0], 'colour_scheme': v[2], 'font_size': v[1], 'count': 0, 'value': 0.0, 'clicks': 0, 'time': 0})
	
	# Register session variables
	session['layoutType'] = bandit.getVersion()
	layout = session['layoutType'].get('layout')
	colour_scheme = session['layoutType'].get('colourScheme')
	font_size = session['layoutType'].get('fontSize')
	session['clicks'] = 0
	session['time'] = 0

	print "layout type: ", session['layoutType']
	return session['layoutType']

def convert_to_seconds(time):
	dif = time / 1000
	return abs(dif)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, threaded=True)
