from pymongo import MongoClient
from itertools import product
import random
import pickle

"""

Node class used to form the User Preferences Tree

"""        

class Node():
    def __init__(self, version):
        self.version = version
        self.veryNegative = {}
        self.negative = {}
        self.neutral = {}
        self.positive = {}
        self.veryPositive = {}

    def setVeryNegative(self, node, percentage):
        self.veryNegative = {'node': node, 'percentage': percentage}

    def setNegative(self, node, percentage):
        self.negative = {'node': node, 'percentage': percentage}

    def setNeutral(self, node, percentage):
        self.neutral = {'node': node, 'percentage': percentage}

    def setPositive(self, node, percentage):
        self.positive = {'node': node, 'percentage': percentage}

    def setVeryPositive(self, node, percentage):
        self.veryPositive = {'node': node, 'percentage': percentage}

"""

Functions to build the User Preferences tree

"""

def getUsers(query):
    users = []

    for q in query:
        users.append(q.get("user_id"))

    return users

def printTree(root, level):
    # if level == len(versions) - 1:
    if level == 3:
        return "\t"*level + "version" + str(level) + "\n"
    ret = "\t"*level + "version" + str(level) + " " + str(root.veryNegative["percentage"]) + " " + str(root.negative["percentage"]) + " " + str(root.neutral["percentage"]) + " " + str(root.positive["percentage"]) + " " + str(root.veryPositive["percentage"]) + "\n"
    ret += printTree(root.veryNegative["node"], level + 1)
    ret += printTree(root.negative["node"], level + 1)
    ret += printTree(root.neutral["node"], level + 1)
    ret += printTree(root.positive["node"], level + 1)
    ret += printTree(root.veryPositive["node"], level + 1)

    return ret

def buildBranch(root, rating, version_no, users, prev_percentage):
    # Get records where the given subset of users rated the current version with 1
    query = db.Ratings2.find(({"$and": [{"layout": versions[version_no][0]}, {"font_size": versions[version_no][1]}, {"colour_scheme": versions[version_no][2]}, {"rating": rating}, {"user_id": {"$in": users }}]}))
    # Calculate percentage of users who gave the version a rating of 1
    percentage = 0.0 if len(users) == 0 else float(query.count()) / float(len(users))
    percentage += prev_percentage
    # Find users who rated version with 1
    new_users = getUsers(query)
    # Add branch to tree
    # Split per ratings
    if rating == 1:
        # Very Negative
        root.setVeryNegative(buildNode(version_no + 1, new_users), percentage)
    elif rating == 2:
        # Negative
        root.setNegative(buildNode(version_no + 1, new_users), percentage)
    elif rating == 3:
        # Neutral
        root.setNeutral(buildNode(version_no + 1, new_users), percentage)
    elif rating == 4:
        # Positive
        root.setPositive(buildNode(version_no + 1, new_users), percentage)
    elif rating == 5:
        # Very Positive
        root.setVeryPositive(buildNode(version_no + 1, new_users), percentage)
    
    return percentage

def buildNode(version_no, users):
    if (version_no == len(versions) - 1):
        return

    # Initialise node for the current version
    root = Node(versions[version_no])

    prev_percentage = 0.0
    for i in range(1,6):
        # Rating 1 branch (Very Negative)
        prev_percentage = buildBranch(root, i, version_no, users, prev_percentage)

    return root


def buildTree():
    users = db.Ratings2.distinct("user_id")
    root = buildNode(0, users)

    print root.veryNegative, root.negative, root.neutral, root.positive, root.veryPositive
    print printTree(root, 0)

    return root

"""

Utility function to save objects into static files
And read them from the files

"""  

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def getTree(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)

    return obj


def averageRating():
    s = 0
    for v in versions:
        query = db.Ratings2.find({"$and": [{"layout": v[0]}, {"font_size": v[1]}, {"colour_scheme": v[2]}]})
        avg = db.Ratings2.aggregate([{ "$match": {
                "$and": [
                    {"layout": v[0]},
                    {"font_size": v[1]},
                    {"colour_scheme": v[2]}
                ]
            } },
            { "$group": { "_id" : None, "sum" : { "$sum": "$rating" } } }], useCursor=False);
        avg = list(avg)
        s += float(avg[0]["sum"]) / query.count()
        print v, float(avg[0]["sum"]) / query.count()
    print "total avg: ", float(s) / len(versions)

"""

Main section

"""

# # Set MongoDB details
# client = MongoClient('localhost:27017')
# # DB for registering user ratings
# db = client.RatingData

# # Layout features and options
# layouts = ["grid", "list"]
# font_sizes = ["small", "large"]
# colour_schemes = ["dark", "light"]
# features = [layouts, font_sizes, colour_schemes]

# versions = list(product(features[0], features[1], features[2]))
# # Add empty version to serve as leaf node
# versions.append(())
# # # print versions

# # averageRating()


# # Build tree of preferences from exisiting real user data
# treeRoot = buildTree()

# # Save Tree object to static file
# save_object(treeRoot, "UserPreferencesTree.pkl")
