import random

class Pool():
    user_pool = {}
    seconds_active=60
    max_users = 50

def getRandom(user_pool):
    return random.choice(list(user_pool.keys()))