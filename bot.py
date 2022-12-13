import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from gtts import gTTS

load_dotenv()

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
token = os.getenv('TOKEN')

@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))


@bot.command()
async def hello(ctx):
    # Checking to make sure the bot (client.user) is not the one that sent the message (message.author)
    if ctx.author == bot.user:
        return
    await ctx.send('Hello!')

bot.run(token)