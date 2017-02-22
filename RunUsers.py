import subprocess
import random
from flask_pymongo import PyMongo
from pymongo import MongoClient
import matplotlib.pyplot as plt

# 10k fake users
# 63% have a bias for light
# 37% for dark
# 23% for small
# 77% for large
# in this case the obvious best version is light + large

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

def plotResults(simulations, horizon, cumulative_rewards, rewards):
	percentages = [0.0 for i in range(simulations)]
	for i in range(simulations):
		percentages[i] = (cumulative_rewards[i*horizon + horizon - 1] / horizon) * 100
	print percentages
	plt.plot([i for i in range(simulations)], percentages)
	plt.axis([0, simulations, 0, 100])
	plt.show()

horizon = 10
simulations = 50
cumulative_rewards =[0.0 for i in range(horizon * simulations)]
rewards = [0.0 for i in range(horizon * simulations)]
sim_no = 0 

for i in range(simulations):
	sim_no += 1
	for j in range(horizon):
		index = (sim_no - 1) * horizon + j
		# create user object
		user = User()
		# Set colour scheme preference
		if random.random() < 0.6:
			# bias for light colour schemes
			user.setColour("light")
		else:
			# bias for dark colour schemes
			user.setColour("dark")
		# Set font preference
		if random.random() < 0.23:
			# bias for small fonts
			user.setFont("small")
		else:
			# bias for large fonts
			user.setFont("large")
		clicks = random.randint(1, 4)
		print "clicks: ", clicks, user.colour, user.font
		casper_script = subprocess.Popen(["casperjs", "button-click.js", user.layout, user.colour, user.font, str(clicks)], stdout=subprocess.PIPE)
		output = casper_script.stdout.read().strip()
		print "output :", output
		reward = 0.0
		if output == "1":
			reward = 1.0
		print reward
		rewards[index] = reward
		if j == 0:
			cumulative_rewards[index] = reward
		else:
			cumulative_rewards[index] = reward + cumulative_rewards[index - 1]
		# subprocess.call(["casperjs", "button-click.js", user.layout, user.colour, user.font, str(clicks)])
print rewards
print cumulative_rewards
plotResults(simulations, horizon, cumulative_rewards, rewards)

