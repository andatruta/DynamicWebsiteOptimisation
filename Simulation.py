import subprocess
import random
from flask_pymongo import PyMongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
from EpsilonGreedy import EpsilonGreedy

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

def plotResults(simulations, horizon, rewards):
	percentages = [0.0 for i in range(simulations)]
	for i in range(simulations):
		percentages[i] = avg_rewards[i] * 100
	print percentages
	plt.plot([i for i in range(simulations)], percentages)
	plt.axis([0, simulations, 0, 100])
	plt.show()

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

# Simulation variables
horizon = 50
simulations = 100
avg_rewards =[0.0 for i in range(simulations)]
rewards = [0.0 for i in range(horizon * simulations)]
sim_no = 0 
epsilon = 0.3

# Website variables
layouts = ["grid", "list"]
font_sizes = ["small", "large"]
colour_schemes = ["dark", "light"]
# colour_schemes = ["light"]
features = [layouts, font_sizes, colour_schemes]

for i in range(simulations):
	for j in range(horizon):
		index = i * horizon + j
		# create user object
		user = User()
		# Set colour scheme preference
		if random.random() < 0.7:
			# bias for light colour schemes
			user.setColour("light")
		else:
			# bias for dark colour schemes
			user.setColour("dark")
		# Set font preference
		if random.random() < 0.3:
			# bias for small fonts
			user.setFont("small")
		else:
			# bias for large fonts
			user.setFont("large")
		# Random number of clicks the user will perform if they like the website
		clicks = random.randint(1, 4)
		# Get layout version from Bandit algorithm
		bandit = EpsilonGreedy(epsilon, features)
		version = bandit.getVersion()
		print "version: ", version
		print "user: ", user.layout, user.colour, user.font
		layout = version.get('layout')
		colour_scheme = version.get('colourScheme')
		font_size = version.get('fontSize')
		if (user.layout == "" or user.layout == layout) and (user.colour == "" or user.colour == colour_scheme) and (user.font == "" or user.font == font_size):
			reward = 1.0
			# db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': clicks})
			db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': 1})
		else:
			reward = 0.0
			db.Clicks.insert_one({'layout': layout, 'colour_scheme': colour_scheme, 'font_size': font_size, 'clicks': 0})
		print reward
		rewards[index] = reward
		avg_rewards[i] += reward
		# subprocess.call(["casperjs", "button-click.js", user.layout, user.colour, user.font, str(clicks)])
	avg_rewards[i] = avg_rewards[i] / horizon
print avg_rewards
file = open("simulation.txt", "w")
file.write(epsilon)
for r in avg_rewards:
  file.write("%s\n" % r)

f.close()
plotResults(simulations, horizon, avg_rewards)
