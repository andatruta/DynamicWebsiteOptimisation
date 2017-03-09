from flask_pymongo import PyMongo
from pymongo import MongoClient
from itertools import product
import random as rand
import math

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

class IteratingBandit():
	def __init__(self, features):
		self.versions = list(product(features[0], features[1], features[2]))
		self.counts = self.getCounts()

	def getCounts(self):
		counts = [0 for version in self.versions]
		for i, version in enumerate(self.versions):
			q_a = db.Clicks.find_one({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}]})
			if q_a != None:
				counts[i] = q_a.get("count")
		return counts

	def updateCount(self, version):
		action = db.Clicks.find_one({"$and": [{"layout": version.get("layout")}, {"font_size": version.get("fontSize")}, {"colour_scheme": version.get("colourScheme")}]})
		k = float(action.get("count"))
		_id = action.get("_id")
		db.Clicks.update_one({"_id": _id},{"$set": {"count": k + 1}}, upsert=False)
		self.counts = self.getCounts()

	def chooseArm(self):
		n_versions = len(self.versions)
		# ensure that each version was shown at least once
		for v in range(n_versions):
			if self.counts[n_versions - 1] == max(self.counts):
				return 0
			elif self.counts[v] != max(self.counts):
				return v

	def getVersion(self):
		v = self.chooseArm()
		# print "counts: ", self.counts
		# print "values: ", self.actionValues
		# print "chosen version: ", v
		return {"layout": self.versions[v][0], "fontSize": self.versions[v][1], "colourScheme": self.versions[v][2]}
