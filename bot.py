import discord
import os
import asyncio
from gtts import gTTS
from dotenv import load_dotenv
from discord.ext import commands
from gtts import gTTS
from mutagen.mp3 import MP3
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

@bot.event
async def on_voice_state_update(member, before, after):
    voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
    if before.channel != after.channel and member.id != bot.application_id and not (voice_client and voice_client.is_connected()):
        if(after.channel is None and before.channel and before.channel.members and len(before.channel.members) > 0):
            message = member.display_name + " disconnected"
            await playTTS(before.channel, message)
        elif after.channel:
            message = member.display_name + " joined " + after.channel.name
            await playTTS(after.channel, message)


@bot.command()
async def tts(ctx, *, text1:str):
    # Checking to make sure the bot (client.user) is not the one that sent the message (message.author)
    if ctx.author == bot.user:
        return
    if not (ctx.author.voice and ctx.author.voice.channel):
        await ctx.send("Please join a voice channel first")
        return
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.author.guild)
    if voice_client and voice_client.is_connected():
        await ctx.send("Please wait until I am finished speaking.")
        return
    await playTTS(ctx.author.voice.channel, text1)

async def playTTS(voiceChannel, text1: str):
    vc = await voiceChannel.connect()
    speech = gTTS(text = text1, lang = 'en', slow = False)
    cwd = os.getcwd()
    audioFilePath = cwd + "/audio.mp3"
    speech.save(audioFilePath)
    vc.play(discord.FFmpegPCMAudio(audioFilePath), after=lambda e: print("done playing tts"))
    audio = MP3(audioFilePath)
    await asyncio.sleep(audio.info.length)
    await vc.disconnect()

bot.run(token)