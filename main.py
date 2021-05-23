#Imports and Libraries
import os
import csv
import random
import discord
import aiohttp
import requests
import youtube_dl
import time
from threading import Timer
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from discord.ext import commands

# Load environment variables from .ENV file
load_dotenv()

# python3 main.py

# Intents to allow on_member_join event
intents = discord.Intents.default()
intents.members = True

# Initialize bot client with the TOKEN variable from .ENV
client = commands.Bot(command_prefix = '$', help_command = None, intents=intents)
MAIN_TOKEN = os.getenv('TOKEN')
botID = os.getenv('BOTID')

# Detects when a member joins the server. A random meme welcomes the member.
@client.event
async def on_member_join(member):
    # Specific guild (server) and channel IDs for the bot
    guild_id = 845488024229380146
    guild = client.get_guild(guild_id)

    channel_id = 845488024673845259
    channel = guild.get_channel(channel_id)

    await channel.send("ur welcoming meme ;)")

    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/memes.json") as r:
            # Use a JSON query and extract a random meme from the returned memes
            memes = await r.json()
            embed = discord.Embed(
                color = discord.Color.orange()
            ) 
            embed.set_image(url=memes["data"]["children"][random.randint(0,25)]["data"]["url"])
            embed.set_footer(text=f"Welcome to the server XD")
            await channel.send(embed=embed)

# Detects when the Discord bot joins a server and sends an appropriate notification to the terminal
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

#The Discord bot joins the voice of the member calling the command.
@client.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        print("dab on them haters")        
        await channel.connect()        
        # server = ctx.guild
        # voice_client = server.voice_client
        # player = await voice_client.create_ytdl_player("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        # players[server.id] = player
        # voice_client.play(source, after)
        # player.start()
    else:
        await ctx.channel.send("NEW not in a vc tsk tsk!")

themeSong = {
    #"userid": "url", 
    553337863031357470: "https://youtu.be/hk1_5NogtZM", # Jamie
    256951017046802432: "https://youtu.be/6ONRf7h3Mdk", #Danny
    832732002842443786: "https://youtu.be/RP1RfkC0u0c", #Jenny 
    320050385698160640: "https://youtu.be/oq4yO5G8eAM" #Razi
}

'''
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
for file in os.listdir("./"):
    if file.endswith(".webm"):
        os.rename(file, "song.webm")
        break
'''

#This commands changes the 'theme song' of the member, which plays when the member enters the same vc as the bot.
@client.command()
async def add(ctx, name, song):
    themeSong[name] = song 
    r = requests.get(song)
    s = bs(r.text, "html.parser")
    print(name)

    # Print to file 
    sourceFile = open('demo.txt', 'w')
    print(s, file = sourceFile)
    sourceFile.close()

    with open("demo.txt") as f:
        lines = f.readlines()
    for line in lines:
        if not line.find("<title>") == -1:
            title = line[line.find("<title>")+7:line.find("</title>")-10]
            break

    ydl_opts = {
        'format': '249/250/251'
    }

    os.remove(str(name)[3:21] + ".webm")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song])
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            if len(file) > 23:
                os.rename(file, str(name)[3:21] + ".webm")
                break

    await ctx.channel.send("\"{0}\" theme song added for {1}".format(str(title), str(name)))
   
# python3 main.py 

'''
# python3 main.py

@client.event
async def on_voice_state_update(member, before, after):    
    botID = 845704608525058099
    if not member.id == botID:
        if before.channel is None and after.channel is not None and not before.channel == after.channel: 
            print("ye")
            
            #await client.join_voice_channel(after.channel)

# python3 main.py
'''

# Prints everyone's theme songs (for debugging purposes)
@client.command()
async def themes(ctx):
    await ctx.channel.send(themeSong) 
    for i in themeSong:
        await ctx.channel.send(str(i) + " " + str(themeSong[i])) 

# In response to a $react message, react with an emoji corresponding to the "feeling" of the sentence
@client.event
async def on_message(message):    
    if message.content.startswith("$react"):
        # Set the correct emotion for the remainder of the sentence
        emotion = sentenceEmotion(message.content)
        if emotion == "anger":
            await message.add_reaction("😡")
        elif emotion == "love":
            await message.add_reaction("💕")
        elif emotion == "joy":
            await message.add_reaction("🤗")
        elif emotion == "fear":
            await message.add_reaction("😱")
        elif emotion == "sadness":
            await message.add_reaction("😢")
        elif emotion == "surprise":
            await message.add_reaction("😲")

# Read in the csv containing the emotion values for each word 
with open('dict.csv') as csv_file:
    reader = csv.reader(csv_file)
    vals = dict(reader)

# Iterate through dictionary and convert each string to an integer array
# it = 0
for key in vals:
    temp = vals[key]
    # Cut off the first and last characters of the 
    # string, which are opening and closing brackets  
    temp = temp[1:-1]
    # if it in range(5): print("TEMPPPPPP!!", temp)
    # Convert the comma separated string to an array
    temp = list(map(float, temp.split(", ")))
    # if it in range(5): print("NEXTTTTTT!!", temp)
    # it += 1
    vals[key] = temp

# Adds the emotion values for each word to determine 
# the predominant emotion in the sentence
def sentenceEmotion(sentence):
    emotionName = ["sadness", "anger", "love", "joy", "fear", "surprise"]
    emotions = [0] * 6
    # Split the sentence into words and delete the 
    # first element, which is "$react" 
    sentence = sentence.split()
    del sentence[0]
    # Sum the emotion values 
    for word in sentence:
        if word in vals:
            for i in range(6):
                emotions[i] += float(vals[word][i])
    # Find the maximum emotion value 
    maximum = 0
    emotion = ""
    for i in range(6):
        if emotions[i] > maximum:
            maximum = emotions[i]
            emotion = emotionName[i]
    print("emotion", emotion)
    return emotion
            
# Prints commands and their functionality 
@client.command()
async def help(ctx):
    # print("hello")
    await ctx.channel.send("""```\nNote: Commands should be used in the form\n\t$name [mandatory params] (optional params).
\nList of Commands:\n\t$add [user ping] [theme song] - Adds a theme song for a user
\t$hello - Says hi!\n\t$help - Displays a list of commands\n\t$join - Joins the user\'s voice channel
\t$leave - Leaves the current voice channel\n\t$react [sentenceword1] (sentenceword2) (...) -\n\t Reacts to the word or sentence sent using one of six emojis.\n
(Type the name of a command followed by the space-separated parameters.)\n```""")

# Say hi!
@client.command()
async def hello(ctx):
    await ctx.channel.send('Hello!')

# Makes Cute-botty leave the call
@client.command()
async def leave(ctx):
    print("Leave")
    # Leave the voice call if it's in one
    if ctx.voice_client:
        server = ctx.guild
        voice_client = server.voice_client
        await ctx.channel.send("Successfully disconnected :)")
        await voice_client.disconnect()
    else:
        await ctx.channel.send("but...but...i'm not in a voice channel ToT")

# Kills the Cute-botty process (for debugging purposes)
@client.command()
async def kill(ctx):
    print("$kill so I leave")
    # Leave call
    if ctx.voice_client:
        server = ctx.guild
        voice_client = server.voice_client
        # await ctx.channel.send("Disconnected 2")
        await voice_client.disconnect()
    # else:
        # await ctx.channel.send("no vc so no dc")
    # Kill 
    # await ctx.channel.send("Dead")
    exit(0)

# Plays theme music for users upon entry to a voice channel 
@client.event
async def on_voice_state_update(member, before, after):    
    # botID = os.getenv('BOTID')

    if not member.id == botID:
        if before.channel is None and after.channel is not None and not before.channel == after.channel: 
            
            #url = "https://www.youtube.com/watch?v=6ONRf7h3Mdk"
            voice = discord.utils.get(client.voice_clients, guild=member.guild)
            voice.stop()

            # Play the correct song with appropriate time delays
            time.sleep(1)
            voice.play(discord.FFmpegPCMAudio(str(member.id) + ".webm"))
            time.sleep(7)
            voice.stop()

# Run the bot using the token previously retrieved from .ENV
client.run(MAIN_TOKEN)