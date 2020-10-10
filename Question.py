from webscraping import *
import discord
import time

ANSWERS_TRIVIA = {0: 'a',
                  1: 'b',
                  2: 'c',
                  3: 'd'}


class Question:
    def __init__(self, ctx):
        self.category, self.difficulty, self.question, self.correct_answer, self.answers, self.typ = webscrap_trivia()
        if "&quot;" in self.question:
            self.question = self.question.replace("&quot;", '"')
        if "&#039;" in self.question:
            self.question = self.question.replace("&#039;", "'")
        self.ctx = ctx
        self.letter = ANSWERS_TRIVIA[self.answers.index(self.correct_answer)]
        self.losers = []
        self.awaiting_answer = False

    def get_question(self):
        return self.question

    def get_awaiting_answer(self):
        return self.awaiting_answer

    def get_category(self):
        return self.category

    def set_ctx(self, ctx):
        self.ctx = ctx

    def get_difficulty(self):
        return self.difficulty

    def get_correct_answer(self):
        return self.correct_answer

    def get_answers(self):
        return self.answers

    def get_typ(self):
        return self.typ

    async def ask_question(self):
        if self.typ == "multiple":
            answers_string = "a. {}\nb. {}\nc. {}\nd. {}".format(*self.answers)
        if self.typ == "boolean":
            answers_string = "a. {}\nb. {}".format(*self.answers)

        if "&quot;" in answers_string:
            answers_string = answers_string.replace("&quot;", '"')
        if "&#039;" in answers_string:
            answers_string = answers_string.replace("&#039;", "'")
        embed_trivia = discord.Embed(
            title=self.question,
            description=answers_string,
            colour=discord.Color.greyple()
        )
        embed_trivia.set_footer(
            text="Category: {} | Difficulty: {} | Time: {}".format(self.category, self.difficulty, "30 seconds"))
        await self.ctx.send(embed=embed_trivia)
        self.awaiting_answer = True

    async def check_answer(self, message, channel, timer):
        end_time = timer + 30
        if not timer >= end_time:
            if message.content in ANSWERS_TRIVIA.values():
                if message.author not in self.losers:
                    if message.content == self.letter:
                        await channel.send("{} is smartest bonobo!".format(message.author.mention))
                        self.ongoing = False
                        return True
                    elif message.content != self.letter:
                        await channel.send("{}, WRONG! You are out!".format(message.author.mention))
                        self.losers.append(message.author)
                        return False
                else:
                    await channel.send("{}, you already answered!".format(message.author.mention))
                    return False
            else:
                return False
        else:
            await channel.send("Time's out!")
            return True
