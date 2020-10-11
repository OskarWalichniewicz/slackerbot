from Question import Question
import discord
from discord.ext import commands
import asyncio


class Trivia(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.question = Question()

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
            await self.timer(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.question is not None:
            if self.question.get_awaiting_answer():
                channel = message.channel
                if await self.question.check_answer(message, channel):
                    self.question = Question()

    async def timer(self, ctx):
        await asyncio.sleep(30)
        await ctx.send("Time's up!\nCorrect answer was: {}. {}".format(self.question.get_letter(), self.question.get_correct_answer()))
        self.question = Question()
        return True


def setup(client):
    client.add_cog(Trivia(client))
