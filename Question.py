from webscraping import *
import discord
import html
from mongoDB import MongoDB

ANSWERS_TRIVIA = {0: 'a',
                  1: 'b',
                  2: 'c',
                  3: 'd'}


class Question:
    def __init__(self):
        self.category, self.difficulty, self.question, self.correct_answer, self.answers, self.typ = webscrap_trivia()
        self.letter = ANSWERS_TRIVIA[self.answers.index(self.correct_answer)]
        self.losers = []
        self.awaiting_answer = False
        self.question = html.unescape(self.question)
        for i in range(len(self.answers)):
            self.answers[i] = html.unescape(self.answers[i])
        self.correct_answer = html.unescape(self.correct_answer)
        self.mongoDB = MongoDB()

    def get_question(self):
        return self.question

    def get_letter(self):
        return self.letter

    def get_awaiting_answer(self):
        return self.awaiting_answer

    def set_awaiting_answer(self, awaiting_answer):
        self.awaiting_answer = awaiting_answer

    def get_category(self):
        return self.category

    def get_difficulty(self):
        return self.difficulty

    def get_correct_answer(self):
        return self.correct_answer

    def get_answers(self):
        return self.answers

    def get_typ(self):
        return self.typ

    async def ask_question(self, ctx):
        if self.typ == "multiple":
            answers_string = "a. {}\nb. {}\nc. {}\nd. {}".format(*self.answers)
        if self.typ == "boolean":
            answers_string = "a. {}\nb. {}".format(*self.answers)

        embed_trivia = discord.Embed(
            title=self.question,
            description=answers_string,
            colour=discord.Color.greyple()
        )
        embed_trivia.set_footer(
            text="Category: {} | Difficulty: {} | Time: {}".format(self.category, self.difficulty, "30 seconds"))
        await ctx.send(embed=embed_trivia)
        self.awaiting_answer = True

    async def check_answer(self, message, channel):
        if message.content.lower() in ANSWERS_TRIVIA.values():
            if message.author not in self.losers:
                if message.content.lower() == self.letter:
                    await channel.send("{} is smartest bonobo!".format(message.author.mention))
                    await self.mongoDB.enter_trivia_data(
                        message.guild.id, message.author.id, message.author.display_name, self.difficulty, True)
                    self.awaiting_answer = False
                    return True
                elif message.content != self.letter:
                    await channel.send("{}, WRONG! You are out!".format(message.author.mention))
                    await self.mongoDB.enter_trivia_data(
                        message.guild.id, message.author.id, message.author.display_name, self.difficulty, False)
                    self.losers.append(message.author)
                    return False
            else:
                await channel.send("{}, you already answered!".format(message.author.mention))
                return False
        else:
            return False
