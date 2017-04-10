from pymongo import MongoClient
from itertools import product
import random
import math
import numpy as np

def getNextUserId():
    return max(db.Ratings2.find().distinct("user_id")) + 1

def createUser(user, diff):
    # print "old user: ", user, "\n"
    new_user = user

    changes = 0

    # randomly choose n=changes versions to change the rating
    while diff != 0 and changes < 8:
        index = random.randint(0, len(new_user) - 1)

        # modify rating by +-1 with uniform probability
        if diff < 0:
            # edge case when rating = 1 - do +1
            if new_user[index]["rating"] == 1:
                new_user[index]["rating"] += 1
                diff -= 1
            else:
                new_user[index]["rating"] = new_user[index]["rating"] - 1
                diff += 1
        elif diff > 0:
            # edge case when rating = 5 - do -1
            if new_user[index]["rating"] == 5:
                new_user[index]["rating"] -= 1
                diff += 1
            else:
                new_user[index]["rating"] += 1
                diff -= 1

        changes += 1

    # print "new_user: ", new_user
    # print "new user total rating: ", sum([version["rating"] for version in new_user]), "\n"

    user_id = getNextUserId()
    for entry in new_user:
        db.Ratings2.insert_one({
            "rating": entry["rating"], 
            "font_size": entry["font_size"], 
            "colour_scheme": entry["colour_scheme"], 
            "layout": entry["layout"], 
            "user_id": user_id, 
            "user_type": "artificial"
        })

def generateArtificialUsers(user, n):
    total = sum([version["rating"] for version in user])
    mean = float(sum([float(version["rating"]) / 5 for version in user])) / len(user)
    var = np.var([float(version["rating"]) / 5 for version in user])
    # print "user id: ", user[0]["user_id"], " mean: ", mean, " var: ", var, " total rating: ", total

    alpha = (math.pow(mean, 2) - math.pow(mean, 3)) / var - mean
    beta = alpha * (1 - mean) / mean

    # print "alpha: ", alpha, " beta: ", beta

    for i in range(n):
        user_mean = np.random.beta(alpha, beta)
        diff = int(round(user_mean*5.0*8.0)) - total

        # if diff > 12:
        #     diff = 12
        # elif diff < -12:
        #     diff = -12

        # print "diff: ", diff

        createUser(user, diff)


# Set MongoDB details
client = MongoClient('localhost:27017')
# DB for registering user ratings
db = client.RatingData

# Get real user ratings
real_users = db.Ratings2.find({"user_type": "real"})

# Get IDs of real users
real_users_ids = real_users.distinct("user_id")

users = []

for i in range(len(real_users_ids)):
    user = db.Ratings2.find({"user_id": real_users_ids[i]})
    users.append(list(user))

# Number of artificial users generated per real user
n = 50

# Create new users with slight deviations from the real users
for user in users:
    # Generate n new users
    generateArtificialUsers(user, n)
