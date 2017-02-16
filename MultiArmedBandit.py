from flask_pymongo import PyMongo
from pymongo import MongoClient
from itertools import product
import random as rand

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

# Global vars
layouts = ["grid", "list"]
font_sizes = ["small", "large"]
colour_schemes = ["dark", "light"]
versions = list(product(layouts, font_sizes, colour_schemes))
epsilon = 0.1

actions = []

for version in versions:
	layout_type = {"layout": version[0], "font_size": version[1], "colour_scheme": version[2]}
	q_a = db.Clicks.find({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}]})
	k_a = q_a.count()
	if k_a == 0:
		k_a = 1
	reward = 0.0
	for a in q_a:
		reward += a.get("clicks")
	actions.append({"layout_type": layout_type, "Q_a": (reward/k_a)})

print [action for action in actions]

# select best action using E-greedy action selection method
# select greedy action
a = actions[0]
if rand.random() < 1 - epsilon:
	a_star = -1.0
	for action in actions:
		if action.get("Q_a") > a_star:
			a_star = action.get("Q_a")
			a = action
else:
	r = rand.randint(len(actions))
	a = actions[r]

print a


