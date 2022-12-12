import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
  
client = discord.Client(intents=discord.Intents.all())
token = os.getenv('TOKEN')

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))


@client.event
async def on_message(message):
    # Checking to make sure the bot (client.user) is not the one that sent the message (message.author)
    if message.author == client.user:
        return

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')

client.run(token)