from Question import Question
import discord
from discord.ext import commands
import asyncio
from mongoDB import MongoDB


class Trivia(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.question = Question()
        mongoDB = MongoDB()
        mongoDB_client = mongoDB.get_client()
        self.db = mongoDB_client.get_database('slacker_db')

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Trivia ready.')

    """
    """
    @commands.command()
    async def trivia(self, ctx):
        if self.question.get_awaiting_answer():
            await ctx.send("There is already one question awaiting answer!")
        else:
            await self.question.ask_question(ctx)
            await self.timer(ctx, self.question)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.question is not None:
            if self.question.get_awaiting_answer():
                channel = message.channel
                if await self.question.check_answer(message, channel):
                    await self.enter_to_mongo(
                        message.guild.id, message.author.id, self.question.get_difficulty(), True)
                    self.question = Question()
                else:
                    await self.enter_to_mongo(message.guild.id, message.author.id, self.question.get_difficulty(), False)

    async def timer(self, ctx, question):
        await asyncio.sleep(30)
        if question is not None and question.get_awaiting_answer():
            await ctx.send("Time's up!\nCorrect answer was: {}. {}".format(question.get_letter(), question.get_correct_answer()))
            self.question = Question()
            return True
        else:
            return False

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
    async def enter_to_mongo(self, server_id, user_id, difficulty, correct):
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


def setup(client):
    client.add_cog(Trivia(client))
