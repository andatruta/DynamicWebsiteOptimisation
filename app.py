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
		return jsonify(status='OK',message='Incremented clicks successfully')

	except Exception,e:
		return jsonify(status='ERROR',message=str(e))

@app.route("/registerSession", methods=['POST'])
def registerSession():
	try:
		layout = session['layoutType'].get('layout')
		colour_scheme = session['layoutType'].get('colourScheme')
		font_size = session['layoutType'].get('fontSize')
		clicks = session['clicks']

		print layout, colour_scheme, font_size, clicks

		db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': clicks})
		return jsonify(status='OK',message='Registered session successfully')
	except Exception,e:
		return jsonify(status='ERROR',message=str(e))

def generate_layout():
	layouts = ["grid", "list"]
	font_sizes = ["small", "large"]
	colour_schemes = ["dark", "light"]
	features = [layouts, font_sizes, colour_schemes]
	bandit = EpsilonGreedy(0.1, features)
	# versions = list(product(layouts, font_sizes, colour_schemes))
	# choice = versions[rand.randint(0, len(versions) - 1)]
	# choice = {'layout': choice[0], 'fontSize': choice[1], 'colourScheme': choice[2]}
	session['layoutType'] = bandit.getVersion()
	session['clicks'] = 0
	print "layout type: ", session['layoutType']
	return session['layoutType']

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)