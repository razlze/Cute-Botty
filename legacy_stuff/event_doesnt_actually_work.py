import discord
import os
from discord.ext import commands 
import youtube_dl
from discord import FFmpegPCMAudio
from dotenv import load_dotenv

# import requests

'''
pip install requests 
pip3 install requests
python -m pip install requests
python3 -m pip install requests
'''

load_dotenv()

# client = discord.Client()
client = commands.Bot(command_prefix = '$')
MAIN_TOKEN = os.getenv('TOKEN')

#get random meme
# def get_meme():
#     meme = requests.get("")

# python3 main.py

# pip install python-dotenv
# python3 -m pip install -U discord.py[voice]

entrymusic = {
    #"userid": "url", 
}

players = {}

# python3 main.py

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
# python3 main.py

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '$hello':
        await message.channel.send('Hello!')
    if message.content == '$join':
        if message.author.voice:
            channel = message.author.voice.channel
            await channel.connect()
            server = message.guild
            voice_client = server.voice_client
            player = await voice_client.create_ytdl_player("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            players[server.id] = player
            # voice_client.play(source, after)
            player.start()
        else:
            await message.channel.send("not in a vc tsk tsk!")
    if message.content == '$leave':
        server = message.guild
        voice_client = server.voice_client
        await message.channel.send("Successfully disconnected :)")
        await voice_client.disconnect()

# command for bot to join vc
# @bot.command(name='leave', help='To make the bot leave the voice channel')

# @client.command(name='join', pass_context=True)
@client.command()
async def join(ctx):
    print("Joineddd")
    channel = ctx.message.author.voice.voice_channel
    await channel.connect()
    # await client.join_voice_channel(channel)

# python3 main.py

@client.event
async def on_voice_state_update(member, before, after):    
    botID = 845704608525058099
    if not member.id == botID:
        if before.channel is None and after.channel is not None and not before.channel == after.channel: 
            print("ye")
            
            #await client.join_voice_channel(after.channel)

# python3 main.py

client.run(MAIN_TOKEN)