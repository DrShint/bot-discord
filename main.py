import discord
import os
from discord.ext import commands
from BOT_MUSIC_SHINT import music

cogs = [music]

client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

for i in range (len(cogs)):
    cogs[i].setup(client)


client.run(os.environ['TOKEN'])