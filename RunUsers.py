import subprocess
import random
from flask_pymongo import PyMongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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

def writeStats(filename, date):
	with open(filename, "a") as file:
		file.write(str(date) + ",")
		versions = db.Clicks.find()
		for i, v in enumerate(versions):
			file.write(str(v.get("percentage")) + ",") if i != versions.count() - 1 else file.write(str(v.get("percentage")))
		file.write("\n")	

	file.close()

# Set MongoDB details
client = MongoClient('localhost:27017')
db = client.ClickData

horizon = 16
simulations = 5
cumulative_rewards =[0.0 for i in range(horizon * simulations)]
rewards = [0.0 for i in range(horizon * simulations)]
sim_no = 0

stats_file = "static/dashboard/data/data.csv"
dt = datetime.now()
stats_date = dt.date()

# open file
# file = open(stats_file, "w")

# headers = "date,"

# versions = db.Clicks.find().count()
# for i in range(versions):
# 	headers += "version" + str(i + 1) if i == versions - 1 else "version" + str(i + 1) + ","
# file.write(headers + '\n')
# file.close()

for i in range(simulations):

	for j in range(horizon):

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
		# Time spent on the website
		time = random.randint(2, 15)
		# Take version screenshot or not
		# capture = True if (i == 0 and j < 8) else False
		capture = False

		# call CasperJS process
		casper_script = subprocess.Popen(["casperjs", "button-click.js", user.layout, user.colour, user.font, str(clicks), str(time), str(capture), str(j + 1)], stdout=subprocess.PIPE)
		output = casper_script.stdout.read().strip()
		print "output :", output
		# subprocess.call(["casperjs", "button-click.js", user.layout, user.colour, user.font, str(clicks)])
	
	# write to Stats file - considering each horizon iteration to be one day
	writeStats(stats_file, stats_date)

	# increment date
	stats_date += timedelta(days=1)


