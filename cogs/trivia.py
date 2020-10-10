import discord
from discord.ext import commands
from webscraping import *

answers = {0: "🇦",
           1: "🇧",
           2: "🇨",
           3: "🇩"}


class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Trivia ready.')

    @commands.command()
    async def trivia(self, ctx):
        category, difficulty, question, correct_answer_str, answers, typ = websccrap_trivia()
        correct_answer_index = answers.index(correct_answer_str)
        if typ == "multiple":
            answers_str = "a. {}\nb. {}\nc. {}\nd. {}".format(*answers)
        if typ == "boolean":
            answers_str = "a. {}\nb. {}".format(*answers)
        embed_trivia = discord.Embed(
            title=question,
            description=answers_str,
            colour=discord.Color.blurple()
        )
        embed_trivia.set_footer(
            text="Category: {} | Difficulty: {} | Time: {}".format(category, difficulty, "30 seconds"))

        msg = await ctx.send(embed=embed_trivia)
        await msg.add_reaction('🇦')
        await msg.add_reaction('🇧')
        if typ == "multiple":
            await msg.add_reaction('🇨')
            await msg.add_reaction('🇩')

        def check(reaction):
            return str(reaction.emoji) == answers[correct_answer_index]

        try:
            reaction, user_answered = await client.wait_for('reaction_add', check=check_game_start, timeout=30)
            await ctx.send("Congrats, {} won!".format(user_answered.mention()))
        except asyncio.TimeoutError:
            await ctx.send("No one answered :(")
            return False


def setup(client):
    client.add_cog(Graveyard(client))
