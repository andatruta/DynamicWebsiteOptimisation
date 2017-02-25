from flask_pymongo import PyMongo
from pymongo import MongoClient
from itertools import product
import random as rand
import math

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

def chooseVersion(p):
	r = rand.random()
	cumulative_p = 0.0
	for i in range(len(p)):
		p_i = p[i]
		cumulative_p += p_i
		if cumulative_p > r:
			return i

class Softmax():
	def __init__(self, temperature, features):
		self.temperature = temperature
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
		new_value = q + 1 / (k + 1) * (reward - q)
		_id = action.get("_id")
		db.Clicks.update_one({"_id": _id},{"$set": {"count": k + 1, "value": new_value}}, upsert=False)
		self.actionValues = self.getActionValues()
		self.counts = self.getCounts()


	def getVersion(self):
		nominator = sum([math.exp(v / self.temperature) for v in self.actionValues])
		probabilities = [math.exp(v / self.temperature) / nominator for v in self.actionValues]
		v = chooseVersion(probabilities)
		# print "version index: ", v
		return {"layout": self.versions[v][0], "fontSize": self.versions[v][1], "colourScheme": self.versions[v][2]}
 