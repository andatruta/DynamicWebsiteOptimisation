from flask_pymongo import PyMongo
from pymongo import MongoClient
from itertools import product
import random as rand

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

class MOEpsilonGreedy():
	def __init__(self, epsilon, features):
		self.epsilon = epsilon
		self.versions = list(product(features[0], features[1], features[2]))
		# print "versions: ", self.versions
		self.counts = self.getCounts()
		self.actionValues = self.getActionValues()

	def getCounts(self):
		counts = [0 for version in self.versions]
		for i, version in enumerate(self.versions):
			q_a = db.Clicks.find_one({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}]})
			if q_a != None:
				counts[i] = q_a.get("count")
		# print "counts: ", counts
		return counts

	def getActionValues(self):
		actionValues = [0.0 for version in self.versions]
		for i, version in enumerate(self.versions):
			q_a = db.Clicks.find_one({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}]})
			if q_a != None:
				actionValues[i] = q_a.get("value")
		# print "values: ", actionValues
		return actionValues

	def updateValue(self, version, reward):
		action = db.Clicks.find_one({"$and": [{"layout": version.get("layout")}, {"font_size": version.get("fontSize")}, {"colour_scheme": version.get("colourScheme")}]})
		q = float(action.get("value"))
		k = float(action.get("count"))

		clicks = action.get("clicks")
		time = action.get("time")

		# perform linear scalarization
		# weight vector
		w = [1, 1]
		# scalarize current reward
		r = w[0] * reward["clicks"] + w[1] * reward["time"]

		# Calculate new value 
		new_value = q + 1 / (k + 1) * (r - q)
		# new_value = ((k - 1) / float(k)) * q + ( 1 / float(k)) * r
		# print "new value: ", new_value

		# Update DB record
		_id = action.get("_id")
		db.Clicks.update_one({"_id": _id},{"$set": {"count": k + 1, "value": new_value, "clicks": clicks + reward["clicks"], "time": time + reward["time"]}}, upsert=False)
		# Update counts and values
		self.actionValues = self.getActionValues()
		self.counts = self.getCounts()

	def updateCount(self, version):
		action = db.Clicks.find_one({"$and": [{"layout": version.get("layout")}, {"font_size": version.get("fontSize")}, {"colour_scheme": version.get("colourScheme")}]})
		k = float(action.get("count"))
		_id = action.get("_id")
		db.Clicks.update_one({"_id": _id},{"$set": {"count": k + 1}}, upsert=False)
		self.counts = self.getCounts()

	def greedyAction(self):
		greedy = max(self.actionValues)
		# print "greedy: ", greedy, self.actionValues.index(greedy), self.actionValues
		return self.actionValues.index(greedy)

	def chooseArm(self):
		if rand.random() < 1 - self.epsilon:
			# print "greedy action"
			return self.greedyAction()
		else:
			# print "random action"
			return rand.randint(0, len(self.actionValues) - 1)

	def getVersion(self):
		v = self.chooseArm()
		return {"layout": self.versions[v][0], "fontSize": self.versions[v][1], "colourScheme": self.versions[v][2]}
