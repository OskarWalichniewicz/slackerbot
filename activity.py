import discord
from discord.ext import commands
from bot import client
import asyncio

async def status_task(wait_time):
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