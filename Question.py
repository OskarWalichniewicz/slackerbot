from webscraping import *
import discord

ANSWERS_TRIVIA = {0: 'a',
                  1: 'b',
                  2: 'c',
                  3: 'd'}


class Question:
    def __init__(self, ctx):
        self.category, self.difficulty, self.question, self.correct_answer, self.answers, self.typ = webscrap_trivia()
        self.client = client
        self.letter = ANSWERS_TRIVIA[self.answers.index(self.correct_answer)]
        self.losers = []
        self.ongoing = True

    def get_question(self):
        return self.question

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

    async def ask_question(self):
        if self.typ == "multiple":
            answers_string = "a. {}\nb. {}\nc. {}\nd. {}".format(*answers)
        if self.typ == "boolean":
            answers_string = "a. {}\nb. {}".format(*answers)
        embed_trivia = discord.Embed(
            title=question,
            description=answers_str,
            colour=discord.Color.blurple()
        )
        embed_trivia.set_footer(
            text="Category: {} | Difficulty: {} | Time: {}".format(category, difficulty, "30 seconds"))
        await self.ctx.send(embed=embed_trivia)

    async def check_answer(self, answer):
        if answer.author not in self.losers:
            if answer == self.letter:
                await self.ctx.send("{} is smartest bonobo!".format(answer.author.mention))
                self.ongoing = False
            elif answer != self.letter:
                await self.ctx.send("{}, WRONG! You are out!".format(answer.author.mention))
                self.losers.append(answer.author)
        else:
            await self.ctx.send("{}, you already answered!".format(answer.author.mention))
