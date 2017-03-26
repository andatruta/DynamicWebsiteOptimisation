import subprocess
import random
from itertools import product
from flask_pymongo import PyMongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
from EpsilonGreedy import EpsilonGreedy
from AnnealedEpsilonGreedy import AnnealedEpsilonGreedy
from Softmax import Softmax
from UCB import UCB
from MOEpsilonGreedy import MOEpsilonGreedy
from MOSoftmax import MOSoftmax
from datetime import datetime, timedelta
from UserPreferences import Node, getTree
from User import User

def writeStats(filename, date):
	with open(filename, "a") as file:
		file.write(str(date) + ",")
		versions = db.Clicks.find()
		for i, v in enumerate(versions):
			file.write(str(v.get("percentage")) + ",") if i != versions.count() - 1 else file.write(str(v.get("percentage")))
		file.write("\n")	

	file.close()

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

# Simulation variables
horizon = 20
simulations = 10
avg_rewards =[0.0 for i in range(simulations)]
epsilon = [0.1]
algos = ["ucb"]

# Website variables
layouts = ["grid", "list"]
# layouts = ["grid"]
font_sizes = ["small", "large"]
colour_schemes = ["dark", "light"]
# colour_schemes = ["light"]
features = [layouts, font_sizes, colour_schemes]

stats_file = "static/dashboard/data/data.csv"
dt = datetime.now()
stats_date = dt.date()

# open file
file = open("simulation.txt", "w")

for algo in algos:
	# initialise all possible versions into DB
	versions = list(product(features[0], features[1], features[2]))
	headers = "date,"

	for i, v in enumerate(versions):
		if db.Clicks.find({"$and": [{"layout": v[0]}, {"font_size": v[1]}, {"colour_scheme": v[2]}]}).count() == 0:
			db.Clicks.insert_one({'layout': v[0], 'colour_scheme': v[2], 'font_size': v[1], 'count': 0, 'value': 0.0, 'clicks': 0, 'time': 0, 'percentage': 0})
		headers += "version" + str(i + 1) if i == len(versions) - 1 else "version" + str(i + 1) + ","
	
	# write all versions to Stats file
	# "w" is overwriting the current file
	f = open(stats_file, "w")
	f.write(headers + "\n")
	f.close()

	# Choose algo type
	if algo == "e-greedy":
		bandit = MOEpsilonGreedy(0.1, features)
	elif algo == "softmax":
		bandit = MOSoftmax(0.1, features)
	elif algo == "ucb":
		bandit = UCB(features)

	for i in range(simulations):
		reward_sum = 0.0

		for j in range(horizon):

			# create user object
			user = User()
			# get preferences tree
			tree = getTree("UserPreferencesTree.pkl")
			# set preferences
			user.buildPreferences(tree, versions)

			# # Random number of clicks the user will perform if they like the website
			# clicks = random.randint(1, 4)
			# # Time spent on the website
			# time = random.randint(2, 8)

			# Get layout version from Bandit algorithm
			version = bandit.getVersion()
			layout = version.get('layout')
			colour_scheme = version.get('colourScheme')
			font_size = version.get('fontSize')

			rating = 0
			for v in user.preferences:
				if v["version"][0] == layout and v["version"][1] == font_size and v["version"][2] == colour_scheme:
					rating = v["rating"]

			print "rating: ", rating

			rewards = {"clicks": rating, "time": rating*5}

			bandit.updateValue(version, rewards)
			# print "reward: ", reward
			# rewards[index] = reward
			reward_sum += rating

		# calculate average reward for simulation
		avg_rewards[i] = reward_sum / float(horizon)
		print i, avg_rewards[i]

		# write to Stats file - considering each horizon iteration to be one day
		writeStats(stats_file, stats_date)

		# increment date
		stats_date += timedelta(days=1)

	# write to Simulation file
	results = ""
	for r in avg_rewards:
		results += str(r)
		results += " "
	file.write(results + "\n")
	print "overall avg reward: ",  float(sum(avg_rewards)) / float(simulations)

	# clear DB for next epsilon simulation
	# db.Clicks.drop()

# close file
file.close()
# plotResults(simulations, horizon, "simulation.txt")
