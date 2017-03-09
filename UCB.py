from flask_pymongo import PyMongo
from pymongo import MongoClient
from itertools import product
import random as rand
import math

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

class UCB():
	def __init__(self, features):
		self.versions = list(product(features[0], features[1], features[2]))
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
		p = float(action.get("percentage"))
		clicks = action.get("clicks")
		time = action.get("time")

		# perform linear scalarization
		# weight vector
		w = [1, 0.5]
		# scalarize current reward
		r = w[0] * reward["clicks"] + w[1] * reward["time"]

		# Calculate new value 
		new_value = q + 1 / (k + 1) * (r - q)
		r_p = 100.0 if reward["clicks"] > 0 else 0.0
		new_percentage = p + 1 / (k + 1) * (r_p - p)
		# new_value = ((k - 1) / float(k)) * q + ( 1 / float(k)) * r

		# Update DB record
		_id = action.get("_id")
		db.Clicks.update_one({"_id": _id},{"$set": {"count": k + 1, "value": new_value, "clicks": clicks + reward["clicks"], "time": time + reward["time"], "percentage": new_percentage}}, upsert=False)
		self.actionValues = self.getActionValues()
		self.counts = self.getCounts()

	def chooseArm(self):
		n_versions = len(self.versions)
		# ensure that each version was shown at least once
		for v in range(n_versions):
			if self.counts[v] == 0:
				return v

		ucb = [0.0 for version in self.versions]
		sum_counts = sum(self.counts)
		# calculate special UCB values
		for v in range(n_versions):
			ucb[v] = self.actionValues[v] + math.sqrt((2 * math.log(sum_counts)) / float(self.counts[v]))
		# print "ucb values: ", ucb

		# return version with maximum UCB value
		return maxValue(ucb)

	def getVersion(self):
		v = self.chooseArm()
		# print "counts: ", self.counts
		# print "values: ", self.actionValues
		# print "chosen version: ", v
		return {"layout": self.versions[v][0], "fontSize": self.versions[v][1], "colourScheme": self.versions[v][2]}

# Helper functions
# Return the index of the maximum value in an array
def maxValue(array):
	max_val = max(array)
	# print "greedy: ", greedy, self.actionValues.index(greedy), self.actionValues
	return array.index(max_val)

