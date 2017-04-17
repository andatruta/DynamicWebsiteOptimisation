import subprocess
import random
from itertools import product
from flask_pymongo import PyMongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
from EpsilonGreedy import EpsilonGreedy
from AnnealedEpsilonGreedy import AnnealedEpsilonGreedy
from Softmax import Softmax
from AnnealedSoftmax import AnnealedSoftmax

class User:
	def __init__(self):
		self.layout = ""
		self.colour = ""
		self.font = ""

	def setLayout(self, layout):
		self.layout = layout

	def setColour(self, colour):
		self.colour = colour

	def setFont(self, font):
		self.font = font

def run_simulations(e):
	sim_rewards = []

	for i in range(simulations):
		# print "db initial count: ", db.Clicks.count()
		versions = list(product(features[0], features[1], features[2]))
		for v in versions:
			db.Clicks.insert_one({'layout': v[0], 'colour_scheme': v[2], 'font_size': v[1], 'count': 0, 'value': 0.0})
		# initialise bandit
		# bandit = EpsilonGreedy(e, features)
		bandit = AnnealedSoftmax(e, features)
		# initialise array of rewards for this bandit
		reward_array = [0.0 for n in range(horizon)]

		for j in range(horizon):
			# index = i * horizon + j
			# create user object
			user = User()
			# Set colour scheme preference
			if random.random() < 0.7:
				# bias for light colour schemes
				user.setColour("light")
				# user.setFont("large")
			else:
				# bias for dark colour schemes
				user.setColour("dark")
			# Set font preference
			if random.random() < 0.75:
				# bias for small fonts
				user.setFont("large")
			else:
				# bias for large fonts
				user.setFont("large")
			# Set layout preference
			if random.random() < 0.55:
				# bias for grid layout
				user.setLayout("grid")
			else:
				# bias for list layout
				user.setLayout("list")

			# Get layout version from Bandit algorithm
			version = bandit.getVersion()
			# print "version: ", version
			layout = version.get('layout')
			colour_scheme = version.get('colourScheme')
			font_size = version.get('fontSize')
			# # insert version to DB if there is no entry
			# if db.Clicks.find({"$and": [{"layout": layout}, {"font_size": font_size}, {"colour_scheme": colour_scheme}]}).count() == 0:
			# 	db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'count': 0, 'value': 0.0})
			reward = 0.0
			accuracy = 0.0
			if (user.layout == "" or user.layout == layout) and (user.colour == "" or user.colour == colour_scheme) and (user.font == "" or user.font == font_size):
				reward = 1.0
				bandit.updateValue(version, reward)
			else:
				bandit.updateValue(version, reward)
			if (layout == "grid" and font_size == "large" and colour_scheme == "light"):
				accuracy = 1.0
			reward_array[j] = reward
			# reward_array[j] = accuracy
			
		# append the rewards of the current bandit to the overall simulations array
		sim_rewards.append(reward_array)
		# print "sim: ", i, reward_array

		# print "db final count: ", db.Clicks.count()

		# clear DB for next bandit
		db.Clicks.drop()

	# print "complete sim: ", sim_rewards

	return sim_rewards

def calc_avg_rewards(rewards):
	avg_rewards = [0.0 for i in range(horizon)]

	for i in range(horizon):
		avg_rewards[i] = sum([rewards[sim][i] for sim in range(simulations)]) / float(simulations)

	print "avg rewards: ", avg_rewards

	return avg_rewards

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

# Simulation variables
horizon = 500
simulations = 1000
epsilon = [0.1]
# epsilon = [0.1, 0.2, 0.3, 0.4, 0.5]

# Website variables
layouts = ["grid", "list"]
# layouts = ["grid"]
font_sizes = ["small", "large"]
colour_schemes = ["dark", "light"]
# colour_schemes = ["light"]
features = [layouts, font_sizes, colour_schemes]

# open file
file = open("simulation.txt", "w")

for e in epsilon:
	# initialise all possible versions into DB	
	print "epsilon: ", e
	sim_rewards = run_simulations(e)
		
	avg_rewards = calc_avg_rewards(sim_rewards)

	# write to file
	# print "avg rewards: ", avg_rewards
	# file.write(str(e) + "\n")
	results = ""
	for r in avg_rewards:
		results += str(r)
		results += " "
	file.write(results + "\n")

# close file
file.close()
# plotResults(simulations, horizon, "simulation.txt")
