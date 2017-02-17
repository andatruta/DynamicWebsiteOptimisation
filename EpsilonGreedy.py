from flask_pymongo import PyMongo
from pymongo import MongoClient
from itertools import product
import random as rand

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

class EpsilonGreedy():
	def __init__(self, epsilon, features):
		self.epsilon = epsilon
		self.versions = list(product(features[0], features[1], features[2]))
		print "versions: ", self.versions
		self.counts = self.getCounts()
		self.actionValues = self.getActionValues()

	def getCounts(self):
		counts = [0 for version in self.versions]
		for i, version in enumerate(self.versions):
			q_a = db.Clicks.find({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}]})
			counts[i] = q_a.count()
		print "counts: ", counts
		return counts

	def getActionValues(self):
		values = [0.0 for version in self.versions]
		for i, version in enumerate(self.versions):
			# layout_type = {"layout": version[0], "font_size": version[1], "colour_scheme": version[2]}
			q_a = db.Clicks.find({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}]})
			reward = 0.0
			# sum up rewards from all of the times the version was shown
			for a in q_a:
				reward += a.get("clicks")
			values[i] = reward / self.counts[i] if self.counts[i] != 0 else 0.0
		print "action values:", values
		return values

	def greedyAction(self):
		greedy = max(self.actionValues)
		return self.actionValues.index(greedy)

	def chooseArm(self):
		if rand.random() < 1 - self.epsilon:
			print "greedy action"
			return self.greedyAction()
		else:
			print "random action"
			return rand.randint(0, len(self.actionValues))

	def getVersion(self):
		v = self.chooseArm()
		return {"layout": self.versions[v][0], "fontSize": self.versions[v][1], "colourScheme": self.versions[v][2]}

# # Global vars
# layouts = ["grid", "list"]
# font_sizes = ["small", "large"]
# colour_schemes = ["dark", "light"]
# versions = list(product(layouts, font_sizes, colour_schemes))
# epsilon = 0.1
# features = [layouts, font_sizes, colour_schemes]

# bandit = EpsilonGreedy(epsilon, features)
# print bandit.chooseArm()

# actions = []

# for version in versions:
# 	layout_type = {"layout": version[0], "font_size": version[1], "colour_scheme": version[2]}
# 	q_a = db.Clicks.find({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}]})
# 	k_a = q_a.count()
# 	if k_a == 0:
# 		k_a = 1
# 	reward = 0.0
# 	for a in q_a:
# 		reward += a.get("clicks")
# 	actions.append({"layout_type": layout_type, "Q_a": (reward/k_a)})

# print [action for action in actions]

# # select best action using E-greedy action selection method
# # select greedy action
# a = actions[0]
# if rand.random() < 1 - epsilon:
# 	a_star = -1.0
# 	for action in actions:
# 		if action.get("Q_a") > a_star:
# 			a_star = action.get("Q_a")
# 			a = action
# else:
# 	r = rand.randint(0, len(actions))
# 	a = actions[r]

# print a


