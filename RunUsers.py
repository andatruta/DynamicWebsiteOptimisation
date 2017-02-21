from subprocess import call
import random
from flask_pymongo import PyMongo
from pymongo import MongoClient

# 10k fake users
# 63% have a bias for red
# 37% for blue
# 23% for 16px
# 77% for20px
# in this case the obvious best version is red + 20px

class User:
	def __init__(self, layout, colour, font):
		self.layout = layout
		self.colour = colour
		self.font = font

	def setLayout(self, layout):
		self.layout = layout

	def setColour(self, colour):
		self.colour = colour

	def setFont(self, font):
		self.font = font

for i in range(20):
	clicks = random.randint(0, 5)
	call(["casperjs", "button-click.js", str(clicks)])