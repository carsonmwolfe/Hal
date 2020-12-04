import difflib
import random
from Command import *
import Commands
from EssentialPackages import *
from Server import Server

print(commands)
print (command)

CREATOR_ID = 653386075095695361
HAL_ID = 663923530626367509

serverinfo = {}
playerinfo = {}

current_time = ""
client = discord.Client()


async def background_loop():
    import datetime
    global currenttime
    while True:
        for server in client.guilds:
            pass


@client.event
async def on_voice_state_update(member,before,after):
    try:
        server = after.channel.guild
    except AttributeError:
        server = before.channel.guild
    user = server.get_member(HAL_ID)
    users = []
    if before !=None and server.get_member(HAL_ID).voice !=None:
        if before.channel != server.get_member(HAL_ID).voice.channel:
            return
    try:
        for user in server.get_member(HAL_ID).voice.channel.members:
            if user.bot == False:
                users.append(user)
        if len(users)==0 and serverinfo[member.guild].currentlyplaying == True:
            server.voice_client.pause()
            print("paused")
    except AttributeError:
        print("Error")


@client.event
async def on_guild_join(server):
    pass


@client.event
async def on_guild_remove(server):
    pass


@client.event
async def on_ready():
    for server in client.guilds:
        serverinfo[server] = Server(server)
        client.loop.create_task(serverinfo[server].update_loop())


@client.event
async def on_message(message):

    if message.content[0]=="*":
        await command[message.content.upper().split(" ")[0]](message,serverinfo,client)


client.run(Token.token)
