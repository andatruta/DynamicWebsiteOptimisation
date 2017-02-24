from flask import Flask, request, render_template, send_file, jsonify, session
from flask_socketio import SocketIO, emit
from flask_pymongo import PyMongo
from flask_uuid import FlaskUUID
from uuid import uuid4
from pymongo import MongoClient
import random as rand
from itertools import product
import json, os
from EpsilonGreedy import EpsilonGreedy

# Create app and PyMongo DB
app = Flask(__name__)
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
bandit = EpsilonGreedy(0.2, features)

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
		bandit.updateValue(session['layoutType'], session['clicks'])
		return jsonify(status='OK',message='Incremented clicks successfully')

	except Exception,e:
		return jsonify(status='ERROR',message=str(e))

def generate_layout():
	# Get layout version from Bandit algorithm
	# bandit = EpsilonGreedy(0.2, features)
	# Register session variables
	bandit = EpsilonGreedy(0.2, features)
	session['layoutType'] = bandit.getVersion()
	session['clicks'] = 0
	layout = session['layoutType'].get('layout')
	colour_scheme = session['layoutType'].get('colourScheme')
	font_size = session['layoutType'].get('fontSize')
	# Register session to DB
	# db.Clicks.insert_one({'session_id': session['uid'], 'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': 0})
	if db.Clicks.find({"$and": [{"layout": layout}, {"font_size": font_size}, {"colour_scheme": colour_scheme}]}).count() == 0:
		db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'count': 1, 'value': 0.0})
	# else increment count
	else:
		bandit.updateCount(session['layoutType'])
	print "layout type: ", session['layoutType'], session['uid']
	return session['layoutType']

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, threaded=True)
