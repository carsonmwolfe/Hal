import os
from EssentialPackages import *
from Command import *
from Music import *
from Footer import get_footer
HAL_ID = 779155599622537226


async def TEST (message,serverinfo,client):
    await message.channel.send("`Test Complete.`")
    

async def RESTART (message,serverinfo,client):
    print ("Restarting...")
    if message.author.id!=CREATOR_ID:
            await message.channel.send("`This Command Is A Creator Only Command.`")
    if message.author.id==CREATOR_ID:
        await message.channel.send("`Hal Is Restarting...`")
        client.loop.run_until_complete(client.logout())
        os.system("python3 /usr/bin/python3.6 /home/pi/Hal.py")
        raise SystemExit
    

command ["*RESTART"] = RESTART
command ["*TEST"] = TEST

for command_name in command.keys():
    commands.append(command_name)
