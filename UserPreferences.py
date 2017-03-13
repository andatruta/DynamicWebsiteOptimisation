from pymongo import MongoClient
from itertools import product

class Node():
	def __init__(self, version):
		self.version = version
		self.veryNegative = {}
		self.negative = {}
		self.neutral = {}
		self.positive = {}
		self.veryPositive = {}

	def setVeryNegative(self, node, percentage):
		self.veryNegative = {'node': version, 'percentage': percentage}

	def setNegative(self, node, percentage):
		self.negative = {'node': version, 'percentage': percentage}

	def setNeutral(self, node, percentage):
		self.neutral = {'node': version, 'percentage': percentage}

	def setPositive(self, node, percentage):
		self.positive = {'node': version, 'percentage': percentage}

	def setVeryPositive(self, node, percentage):
		self.veryPositive = {'node': version, 'percentage': percentage}

def buildTree(versions):
	distribution = []

	for i, version in enumerate(versions):
		query = db.Ratings.find(({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}]}))
		if i == 0:
			root = Node(version)
		rating1 = float(db.Ratings.find(({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}, {"rating": 1}]})).count()) / float(query.count())
		root.setVeryNegative("", rating1)
		rating2 = float(db.Ratings.find(({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}, {"rating": 2}]})).count()) / float(query.count()) + rating1
		root.setNegative("", rating2)
		rating3 = float(db.Ratings.find(({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}, {"rating": 3}]})).count()) / float(query.count()) + rating2
		root.setNeutral("", rating3)
		rating4 = float(db.Ratings.find(({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}, {"rating": 4}]})).count()) / float(query.count()) + rating3
		root.setPositive("", rating4)
		rating5 = float(db.Ratings.find(({"$and": [{"layout": version[0]}, {"font_size": version[1]}, {"colour_scheme": version[2]}, {"rating": 5}]})).count()) / float(query.count()) + rating4
	 	root.setVeryPositive("", rating5)
	 	distribution.append({"version": version, 1: rating1, 2: rating2, 3: rating3, 4: rating4, 5: rating5})

	print root.veryNegative

def addUserId(db, no_versions):
	user_id = 0
	i = 0
	for item in db.Ratings.find():
		db.Ratings.update_one(item, {"$set": {"user_id": user_id,}})

# Set MongoDB details
client = MongoClient('localhost:27017')
# DB for registering user ratings
db = client.RatingData

# Layout features and options
layouts = ["grid", "list"]
font_sizes = ["small", "large"]
colour_schemes = ["dark", "light"]
features = [layouts, font_sizes, colour_schemes]

versions = list(product(features[0], features[1], features[2]))

buildTree(versions)

