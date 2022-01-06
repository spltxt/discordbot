import requests
import time
import discord
import os
#в модуле data содержатся словари для перевода необходимой информации на русский, реалмы и их сокращения
from data import *
from discord.ext import commands

client = commands.Bot(command_prefix='!')
client.remove_command('help')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)


