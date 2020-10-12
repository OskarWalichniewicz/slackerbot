from Question import Question
import discord
from discord.ext import commands
import asyncio
from mongoDB import MongoDB


class Trivia(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.question = Question()
        self.mongo_client = MongoDB()

    def get_all_users(self):

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

    @commands.command()
    async def leaderboard(self, ctx):
        embed_leaderboard = await self.mongo_client.get_leaderboard(ctx)
        await ctx.send(embed=embed_leaderboard)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.question is not None:
            if self.question.get_awaiting_answer():
                channel = message.channel
                if await self.question.check_answer(message, channel):
                    self.question = Question()  # resets

    async def timer(self, ctx, question):
        await asyncio.sleep(30)
        if question is not None and question.get_awaiting_answer():
            await ctx.send("Time's up!\nCorrect answer was: {}. {}".format(question.get_letter(), question.get_correct_answer()))
            self.question = Question()
            return True
        else:
            return False


def setup(client):
    client.add_cog(Trivia(client))
