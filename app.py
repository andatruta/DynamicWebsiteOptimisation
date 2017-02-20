from flask import Flask, request, render_template, send_file, jsonify, session
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
from pymongo import MongoClient
import random as rand
from itertools import product
import json, os
from EpsilonGreedy import EpsilonGreedy

# Create app and PyMongo DB
app = Flask(__name__)
socketio = SocketIO(app)

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

# Set app secret (for sessions).
app.secret_key = os.urandom(24)

@app.route("/")
def index():
	return render_template('index.html', layout=generate_layout())

@app.route("/registerClick", methods=['POST'])
def registerClick():
	try:
		session['clicks'] += 1
		print 'clicks: ', session['clicks']
		# Update MongoDB entry
		db.ProductData.update_one({'_id': session['_id']},{'$set': {'clicks': session['clicks']}}, upsert=False)
		return jsonify(status='OK',message='Incremented clicks successfully')

	except Exception,e:
		return jsonify(status='ERROR',message=str(e))

def generate_layout():
	# Layout features and options
	layouts = ["grid", "list"]
	font_sizes = ["small", "large"]
	colour_schemes = ["dark", "light"]
	features = [layouts, font_sizes, colour_schemes]
	# Get layout version from Bandit algorithm
	bandit = EpsilonGreedy(0.2, features)
	# Register session variables
	session['layoutType'] = bandit.getVersion()
	session['clicks'] = 0
	layout = session['layoutType'].get('layout')
	colour_scheme = session['layoutType'].get('colourScheme')
	font_size = session['layoutType'].get('fontSize')
	# Register session to DB
	session['_id'] = str(db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': 0}).inserted_id)
	print "layout type: ", session['layoutType'], session['clicks']
	return session['layoutType']

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, threaded=True)