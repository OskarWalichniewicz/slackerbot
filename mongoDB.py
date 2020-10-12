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
        self.db = mongoDB_client.get_database('slacker_db')

    def get_client(self):
        return self.client

    """
    {
        "_id":{"$oid":"5f841b92fb86ace89a83afaf"},
        "server_id": "",
        "discord_id":"247438282424713216",
        "easy_correct":{"$numberInt":"0"},
        "easy_answered":{"$numberInt":"0"},
        "medium_correct":{"$numberInt":"0"},
        "medium_answered":{"$numberInt":"0"},
        "hard_correct:{"$numberInt":"0"},
        "hard_answered":{"$numberInt":"0"}
    }
    """
    async def enter_trivia_data(self, server_id, user_id, difficulty, correct):
        records_trivia = self.db.trivia_data
        query = {
            'discord_id': user_id
        }
        # \/ if document exists, we update
        if records_trivia.count_documents(query) > 0:
            record = records_trivia.find_one(query)
            if difficulty == 'easy':
                questions_answered = record['easy_answered']
                questions_answered = questions_answered + 1

                if correct:
                    questions_correct = record['easy_correct']
                    questions_correct = questions_correct + 1
                    update = {
                        'easy_answered': questions_answered,
                        'easy_correct': questions_correct
                    }

                else:
                    update = {
                        'easy_answered': questions_answered,
                    }

                records_trivia.update_one(query, {'$set':  update})

            elif difficulty == 'medium':
                questions_answered = record['medium_answered']
                questions_answered = questions_answered + 1

                if correct:
                    questions_correct = record['medium_correct']
                    questions_correct = questions_correct + 1
                    update = {
                        'medium_answered': questions_answered,
                        'medium_correct': questions_correct
                    }

                else:
                    update = {
                        'medium_answered': questions_answered,
                    }

                records_trivia.update_one(query, {'$set':  update})

            elif difficulty == 'hard':
                questions_answered = record['hard_answered']
                questions_answered = questions_answered + 1

                if correct:
                    questions_correct = record['hard_correct']
                    questions_correct = questions_correct + 1
                    update = {
                        'hard_answered': questions_answered,
                        'hard_correct': questions_correct
                    }

                else:
                    update = {
                        'hard_answered': questions_answered,
                    }

                records_trivia.update_one(query, {'$set':  update})
        # \/ if document doesn't exist
        else:
            if difficulty == 'easy':
                if correct:
                    new_user = {
                        "server_id": server_id,
                        "discord_id": user_id,
                        "easy_correct": 1,
                        "easy_answered": 1,
                        "medium_correct": 0,
                        "medium_answered": 0,
                        "hard_correct": 0,
                        "hard_answered": 0
                    }
                else:
                    new_user = {
                        "server_id": server_id,
                        "discord_id": user_id,
                        "easy_correct": 0,
                        "easy_answered": 1,
                        "medium_correct": 0,
                        "medium_answered": 0,
                        "hard_correct": 0,
                        "hard_answered": 0
                    }

            elif difficulty == 'medium':
                if correct:
                    new_user = {
                        "server_id": server_id,
                        "discord_id": user_id,
                        "easy_correct": 0,
                        "easy_answered": 0,
                        "medium_correct": 1,
                        "medium_answered": 1,
                        "hard_correct": 0,
                        "hard_answered": 0
                    }
                else:
                    new_user = {
                        "server_id": server_id,
                        "discord_id": user_id,
                        "easy_correct": 0,
                        "easy_answered": 0,
                        "medium_correct": 0,
                        "medium_answered": 1,
                        "hard_correct": 0,
                        "hard_answered": 0
                    }

            elif difficulty == 'hard':
                if correct:
                    new_user = {
                        "server_id": server_id,
                        "discord_id": user_id,
                        "easy_correct": 0,
                        "easy_answered": 0,
                        "medium_correct": 0,
                        "medium_answered": 0,
                        "hard_correct": 1,
                        "hard_answered": 1
                    }
                else:
                    new_user = {
                        "server_id": server_id,
                        "discord_id": user_id,
                        "easy_correct": 0,
                        "easy_answered": 0,
                        "medium_correct": 0,
                        "medium_answered": 0,
                        "hard_correct": 0,
                        "hard_answered": 1
                    }
            records_trivia.insert_one(new_user)

    async def get_data(self, collection, query):
        records = self.db.collection

        return records.find_one(query)
