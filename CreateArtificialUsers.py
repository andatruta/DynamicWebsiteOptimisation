from pymongo import MongoClient
from itertools import product
import random

def getNextUserId():
    return max(db.Ratings2.find().distinct("user_id")) + 1

def createUser(user, changes):
    new_user = user

    # randomly choose n=changes versions to change the rating
    for i in range(changes):
        index = random.randint(0, len(new_user) - 1)
        print "change index: ", index
        # modify rating by +-1 with uniform probability
        if random.random() < 0.5:
            # edge case when rating = 1 - do +1
            print "before", new_user[index]["rating"]
            if new_user[index]["rating"] == 1:
                new_user[index]["rating"] += 1
            else:
                new_user[index]["rating"] = new_user[index]["rating"] - 1
                print "after", new_user[index]["rating"]
        else:
            # edge case when rating = 5 - do -1
            if new_user[index]["rating"] == 5:
                new_user[index]["rating"] -= 1
            else:
                new_user[index]["rating"] += 1

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
    for i in range(n):
        p = random.random()
        print "random", p
        # New user within 1 std dev of real user
        if p <= 0.6837:
            changes = 2
        elif p > 0.6837 and p <= 0.9545:
            changes = 4
        else:
            changes = 6
        createUser(user, changes)


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
    print list(user)

# for user in users:
#   print [entry for entry in user]

# Number of artificial users generated per real user
n = 20

# Create new users with slight deviations from the real users
for user in users:
    # Generate n new users
    generateArtificialUsers(user, n)
