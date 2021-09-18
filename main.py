import discord
from discord.ext import commands
from BOT_MUSIC_SHINT import music

cogs = [music]

client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

for i in range (len(cogs)):
    cogs[i].setup(client)


client.run('ODg3ODU2NTU5NTg4MjU3ODcz.YUKO2w.x3zuxxqaIdKJ9oNhs4-OaVxs22g')