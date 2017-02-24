import subprocess
import random
from itertools import product
from flask_pymongo import PyMongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
from EpsilonGreedy import EpsilonGreedy
from AnnealedEpsilonGreedy import AnnealedEpsilonGreedy

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

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

# Simulation variables
horizon = 200
simulations = 100
avg_rewards =[0.0 for i in range(simulations)]
epsilon = [0.1, 0.2, 0.3, 0.4]

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
	versions = list(product(features[0], features[1], features[2]))
	for v in versions:
		db.Clicks.insert_one({'layout': v[0], 'colour_scheme': v[2], 'font_size': v[1], 'count': 0, 'value': 0.0})
	print "epsilon: ", e
	bandit = EpsilonGreedy(e, features)

	for i in range(simulations):
		reward_sum = 0.0

		for j in range(horizon):
			# index = i * horizon + j
			# create user object
			user = User()
			# Set colour scheme preference
			if random.random() < 0.7:
				# bias for light colour schemes
				user.setColour("light")
				user.setFont("large")
			else:
				# bias for dark colour schemes
				user.setColour("dark")
			# Set font preference
			# if random.random() < 0.1:
			# 	# bias for small fonts
			# 	user.setFont("small")
			# else:
			# 	# bias for large fonts
			# 	user.setFont("large")
			# Random number of clicks the user will perform if they like the website
			clicks = random.randint(1, 4)
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
			if (user.layout == "" or user.layout == layout) and (user.colour == "" or user.colour == colour_scheme) and (user.font == "" or user.font == font_size):
				reward = 1.0
				# db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': clicks})
				# db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': 1})
				bandit.updateValue(version, reward)
			else:
				# db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': 0})
				bandit.updateValue(version, 0.0)
			# print "reward: ", reward
			# rewards[index] = reward
			reward_sum += reward

		# calculate average reward for simulation
		avg_rewards[i] = reward_sum / float(horizon)
		print i, avg_rewards[i]

	# write to file
	# print "avg rewards: ", avg_rewards
	# file.write(str(e) + "\n")
	results = ""
	for r in avg_rewards:
		results += str(r)
		results += " "
	file.write(results + "\n")

	# clear DB for next epsilon simulation
	db.Clicks.drop()

# close file
file.close()
# plotResults(simulations, horizon, "simulation.txt")
