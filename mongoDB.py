from pymongo import MongoClient
import os


class MongoDB():
    def __init__(self):
        self.username = str(os.environ['MONGO_USERNAME'])
        self._password = str(os.environ['MONGO_PASSWORD'])
        self.default_database = 'slacker_db'

        mongo_url = "mongodb+srv://{}:{}@slackersdb.nrxyg.mongodb.net/{}?retryWrites=true&w=majority".format(
            self.username, self._password, self.default_database)

        self.client = MongoClient(mongo_url)

    def get_client(self):
        return self.client
