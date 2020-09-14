import discord
from discord.ext import commands
import os
import asyncio
from github_integration import *
from wordofaday import *

client = commands.Bot(command_prefix = '.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

wait_time = 60
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('Milica is a midget'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Dran doesn\'t have mats'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Az is dead'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Cenelia is handsome'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Bobsy is being molested'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Awy is the wisest'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Akcent hates Cene'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Gazda likes Rasta'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Segment is old'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Tesla was croatian'))
        await asyncio.sleep(wait_time)

@client.command()
async def word(ctx):
    english_word = get_word_of_the_day()
    serbian_word_cyr, serbian_word_lat = translate_wotd(english_word, 'sr')
    serbian_word = str(serbian_word_cyr) + " / " + str(serbian_word_lat)
    italian_word = translate_wotd(english_word, 'it')
    dutch_word = translate_wotd(english_word, 'nl')
    polish_word = translate_wotd(english_word, 'pl')
    romanian_word = translate_wotd(english_word, 'ro')

    syns = get_synonyms(english_word)
    print(syns)
    ants = get_antonyms(english_word)
    print(ants)
    def_list = get_definition(english_word)
    print(def_list)

    if len(def_list) == 2:
        word_type = def_list[0]
        definition = def_list[1]

        embed_wotd = discord.Embed(
            title = '{}'.format(english_word.upper()),
            description = word_type + ": " + definition,
            colour = discord.Color.orange()
        )

    elif len(def_list) >= 4:
        word_type = def_list[0]
        definition = def_list[1]
        word_type_2 = def_list[2]
        definition_2 = def_list[3]

        embed_wotd = discord.Embed(
            title = '{}'.format(english_word.upper()),
            description = word_type + ": " + definition + "\n" + word_type_2 + ": " + definition_2,
            colour = discord.Color.orange()
        )
    else:
        embed_wotd = discord.Embed(
            title = '{}'.format(english_word.upper()),
            colour = discord.Color.orange()
        )

    embed_wotd.add_field(name = ':flag_gb: English :flag_gb:', value = english_word, inline = False)
    embed_wotd.add_field(name = ':flag_rs: Serbian :flag_rs:', value = serbian_word, inline = False)
    embed_wotd.add_field(name = ':flag_it: Italian :flag_it:', value = italian_word, inline = False)
    embed_wotd.add_field(name = ':flag_nl: Dutch :flag_nl:', value = dutch_word, inline = False)
    embed_wotd.add_field(name = ':flag_pl: Polish :flag_pl:', value = polish_word, inline = False)
    embed_wotd.add_field(name = ':flag_ro: Romanian :flag_ro:', value = romanian_word, inline = False)

    footer = ""
    if syns is not None:
        footer = "Synonyms: " + syns
        if ants is not None:
            footer += "\n"
            footer += "Antonyms: "
            footer += ants
    else:
        if ants is not None:
            footer = "Antonyms: " + ants

    if footer != "":
        embed_wotd.set_footer(text = footer)

    await ctx.send(embed=embed_wotd)

# schedule.every().day.at("20:00").do()

@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print("Bot ready")

@client.event
async def on_message(message):
    if message.author.id == int(os.environ['AZ_DISCORD_ID']):
        year = message.created_at.year
        month = message.created_at.month
        day = message.created_at.day
        hour = message.created_at.hour
        minute = message.created_at.minute
        second = message.created_at.second
        az_file_input = year + "\n" + month + "\n"+ day + "\n"+ hour + "\n" +minute + "\n"+ second
        az_file = open("az.txt", "w").close()
        az_file = open("az.txt", "w")
        az_file.write(az_file_input)
    if message.content == '.azsave' and message.author.id == 247438282424713216:
        save_to_github(az_file_input)

    await client.process_commands(message)

client.run(os.environ['DISCORD_TOKEN'])