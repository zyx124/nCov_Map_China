from pymongo import MongoClient

uri = "**confidential"
client = MongoClient(uri)
db = client['n_cov']

class DB:
    def __init__(self):
        self.db = db

    def insert(self, collection, data):
        self.db[collection].insert(data)

    def find_one(self, collection, data=None):
        return self.db[collection].find_one(data)