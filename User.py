from pymongo import MongoClient
from itertools import product
import random

"""

User class used to model an artificial user

"""       

class User:
    def __init__(self):
        self.preferences = []

    def addPreference(self, version, rating):
        self.preferences.append({"version": version, "rating": rating})

    def buildPreferences(self, treeRoot, versions):
        root = treeRoot

        # traverse the Preferences Tree
        for i in range(0, len(versions)):
            prob = random.random()
            if prob < root.veryNegative["percentage"]:
                self.addPreference(root.version, 1)
                root = root.veryNegative["node"]
            elif prob >=root.veryNegative["percentage"] and prob < root.negative["percentage"]:
                self.addPreference(root.version, 2)
                root = root.negative["node"]
            elif prob >=root.negative["percentage"] and prob < root.neutral["percentage"]:
                self.addPreference(root.version, 3)
                root = root.neutral["node"]
            elif prob >=root.neutral["percentage"] and prob < root.positive["percentage"]:
                self.addPreference(root.version, 4)
                root = root.positive["node"]
            elif prob >=root.positive["percentage"] and prob < root.veryPositive["percentage"]:
                self.addPreference(root.version, 5)
                root = root.veryPositive["node"]