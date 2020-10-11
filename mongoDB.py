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

    def open_database(self, database_name):
        self.current_database = self.client.get_database(database_name)

    def open_collection(self, collection_name):
        self.records = self.current_database.collection_name

    def get_document(self, query):
        return self.records.find_one(query)

    def update_document(self, query, update):
        self.records.update_one(query, {'$set': update})
