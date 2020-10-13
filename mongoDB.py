from pymongo import MongoClient
import discord
import os


class MongoDB():
    def __init__(self):
        self.username = str(os.environ['MONGO_USERNAME'])
        self._password = str(os.environ['MONGO_PASSWORD'])
        self.default_database = 'slacker_db'

        mongo_url = "mongodb+srv://{}:{}@slackersdb.nrxyg.mongodb.net/{}?retryWrites=true&w=majority".format(
            self.username, self._password, self.default_database)

        self.client = MongoClient(mongo_url)
        self.db = self.client.get_database('slacker_db')

    def get_client(self):
        return self.client

    """
    {
        "_id":{"$oid":"5f841b92fb86ace89a83afaf"},
        "server_id": "",
        "discord_id":"247438282424713216",
        "display_name":"",
        "easy_correct":{"$numberInt":"0"},
        "easy_answered":{"$numberInt":"0"},
        "medium_correct":{"$numberInt":"0"},
        "medium_answered":{"$numberInt":"0"},
        "hard_correct:{"$numberInt":"0"},
        "hard_answered":{"$numberInt":"0"}
    }
    """
    async def enter_trivia_data(self, server_id, user_id, user_display_name, difficulty, correct):
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
                        'easy_correct': questions_correct,
                        'display_name': user_display_name
                    }

                else:
                    update = {
                        'easy_answered': questions_answered,
                        'display_name': user_display_name,
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
                        'medium_correct': questions_correct,
                        'display_name': user_display_name
                    }

                else:
                    update = {
                        'medium_answered': questions_answered,
                        'display_name': user_display_name
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
                        'hard_correct': questions_correct,
                        'display_name': user_display_name
                    }

                else:
                    update = {
                        'hard_answered': questions_answered,
                        'display_name': user_display_name
                    }

                records_trivia.update_one(query, {'$set':  update})
        # \/ if document doesn't exist
        else:
            if difficulty == 'easy':
                if correct:
                    new_user = {
                        "server_id": server_id,
                        "discord_id": user_id,
                        "display_name": user_display_name,
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
                        "display_name": user_display_name,
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
                        "display_name": user_display_name,
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
                        "display_name": user_display_name,
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
                        "display_name": user_display_name,
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
                        "display_name": user_display_name,
                        "easy_correct": 0,
                        "easy_answered": 0,
                        "medium_correct": 0,
                        "medium_answered": 0,
                        "hard_correct": 0,
                        "hard_answered": 1
                    }
            records_trivia.insert_one(new_user)

    """
    """
    async def get_leaderboard(self, user_list):
        PLACE_DICT: {
            0: '🏅',
            1: '🥈',
            2: '🥉'
        }

        records_trivia = self.db.trivia_data
        by_server_id = {
            'server_id': 245250774861479936
        }

        records_list = list(records_trivia.find(by_server_id))  # query list
        leaderboard = []
        for x in range(len(records_list)):
            leaderboard.append({'discord_id': records_list[x]['discord_id'],
                                'display_name': records_list[x]['display_name'],
                                'all_correct': records_list[x]['easy_correct'] + records_list[x]['medium_correct'] + records_list[x]['hard_correct'],
                                'all_answered': records_list[x]['easy_answered'] + records_list[x]['medium_answered'] + records_list[x]['hard_answered']})  # creates list of dictionaries

        sorted_leaderboard = sorted(
            leaderboard, key=lambda k: k['all_correct'] / k['all_answered'], reverse=True)  # calculates winrate and sort (highest 1st)

        sorted_leaderboard = sorted_leaderboard[:10]  # gets first 10 elements

        def get_leaderboard_blueprint_name(index):
            return "{}".format(sorted_leaderboard[index]['display_name'])

        def get_leaderboard_blueprint(index):
            return "{}% winrate! ({} correct out of {} asked)".format(
                round(((sorted_leaderboard[index]['all_correct'] /
                        sorted_leaderboard[index]['all_answered']) * 100), 2),
                sorted_leaderboard[index]['all_correct'],
                sorted_leaderboard[index]['all_answered']
            )

        embed_leaderboard = discord.Embed(
            title='Trivia leaderboard',
            colour=discord.Color.green()
        )
        for x in range(0, len(sorted_leaderboard)):
            if x in PLACE_DICT:
                name = "{} {}".format(
                    PLACE_DICT[x], get_leaderboard_blueprint_name(x))
            else:
                name = "{}".format(get_leaderboard_blueprint_name(x))
            embed_leaderboard.add_field(
                name=name, value=get_leaderboard_blueprint(x), inline=False)

        return embed_leaderboard

    async def get_data(self, collection, query):
        return collection.find_one(query)

    async def update_data(self, records, query, update):
        records.update_one(query, {'$set': update})

    async def open_last_message(self):
        return self.db.last_message

    async def open_trivia_data(self):
        return self.db.trivia_data
