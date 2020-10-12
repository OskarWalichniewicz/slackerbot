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
                    self.enter_to_mongo(
                        message, message.author.id, self.question.get_difficulty())
                    self.question = Question()

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
        "easy_answered":{"$numberInt":"0"},
        "medium_answered":{"$numberInt":"0"},
        "hard_answered":{"$numberInt":"0"}
    }
    """
    async def enter_to_mongo(self, message, user_id, difficulty):
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
                update = {
                    'easy_answered': questions_answered
                }
                records_trivia.update_one(query, {'$set':  update})

            elif difficulty == 'medium':
                questions_answered = record['medium_answered']
                questions_answered = questions_answered + 1
                update = {
                    'medium_answered': questions_answered
                }
                records_trivia.update_one(query, {'$set':  update})

            elif difficulty == 'hard':
                questions_answered = record['hard_answered']
                questions_answered = questions_answered + 1
                update = {
                    'hard_answered': questions_answered
                }
                records_trivia.update_one(query, {'$set':  update})
        # \/ if document doesn't exist
        else:
            server_id = message.guild.id
            if difficulty == 'easy':
                new_user = {
                    "server_id": server_id,
                    "discord_id": user_id,
                    "easy_answered": 1,
                    "medium_answered": 0,
                    "hard_answered": 0
                }

            elif difficulty == 'medium':
                new_user = {
                    "server_id": server_id,
                    "discord_id": user_id,
                    "easy_answered": 0,
                    "medium_answered": 1,
                    "hard_answered": 0
                }

            elif difficulty == 'hard':
                new_user = {
                    "server_id": server_id,
                    "discord_id": user_id,
                    "easy_answered": 0,
                    "medium_answered": 0,
                    "hard_answered": 1
                }
            records_trivia.insert_one(new_user)


def setup(client):
    client.add_cog(Trivia(client))
