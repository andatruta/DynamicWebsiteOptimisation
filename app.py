from flask import Flask, request, render_template, send_file, jsonify
import random as rand
from itertools import product
import json

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html', layout=generate_layout())

def generate_layout():
	layouts = ["grid", "list"]
	font_sizes = ["small", "large"]
	colour_schemes = ["dark", "light"]
	versions = list(product(layouts, font_sizes, colour_schemes))
	choice = versions[rand.randint(0, len(versions) - 1)]
	choice = {'layout': choice[0], 'fontSize': choice[1], 'colourScheme': choice[2]}
	return choice

if __name__ == "__main__":
	app.run(host="localhost", debug=True)