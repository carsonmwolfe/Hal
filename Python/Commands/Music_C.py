import sys
sys.path.append("../")
from EssentialPackages import *
from Command import *
from Music import *
from Footer import get_footer
HAL_ID = 663923530626367509

async def PLAY(message,serverinfo,client):
    serverinfo[message.guild].Leave = False
    serverinfo[message.guild].Skip = False
    serverinfo[message.guild].pause = False
    serverinfo[message.guild].resume = False
    serverinfo[message.guild].songended = False
    serverinfo[message.guild].SongEndedTime = datetime.datetime.now()
    serverinfo[message.guild].LeaveVC = True
    serverinfo[message.guild].MusicAuthor = message.author
    serverinfo[message.guild].paused = False
    channel=message.author.voice.channel
    serverinfo[message.guild].MusicTextChannel = message.channel
    if message.guild.voice_client == None:
        await channel.connect()

    else:
        await message.guild.get_member(HAL_ID).edit(voice_channel = channel)
    if len(serverinfo[message.guild].Queue)<1:
        serverinfo[message.guild].QueueList="\nNo Songs In Queue"
    if serverinfo[message.guild].currentlyplaying == True:
        if channel == None:
            await message.channel.send("`Please join a voice channel to start a song`")
            return
        await message.channel.send("`Song Added To Queue`")
        query_string = urllib.parse.urlencode({"search_query" : " ".join(str(message.content).split(' ')[1:])})
        req = "http://www.youtube.com/results?"+query_string
        with urllib.request.urlopen(req) as html:
            searchresults=re.findall("watch\?v=(.{11})", requests.get(req).text)
            link = ("http://www.youtube.com/watch?v=" + searchresults[0])
            QueueInfo = await YTDLSource.from_url(link,loop = client.loop)
            print (QueueInfo.title)
            url = (link)
        if "youtube.com" in url:
            from bs4 import BeautifulSoup
            page=requests.get(url).text
            soup=BeautifulSoup(page,features='html.parser')
            name=soup.find('meta',{'property':'og:title'})['content']
            serverinfo[message.guild].Queue.append([name,url])
            serverinfo[message.guild].QueueList = ""
            for x in serverinfo[message.guild].Queue:
                serverinfo[message.guild].QueueList += "\n" + "["+ str(x[0])+ "]" + "("+str(x[1])+")"

    if serverinfo[message.guild].currentlyplaying == False:
        serverinfo[message.guild].currentlyplaying = True
        serverinfo[message.guild].LeaveVC = False
        if channel == None:
            await message.channel.send("`Please join a voice channel to start a song`")
            return
        query_string = urllib.parse.urlencode({"search_query" : " ".join(str(message.content).split(' ')[1:])})
        req = "http://www.youtube.com/results?"+query_string
        with urllib.request.urlopen(req) as html:
            searchresults=re.findall("watch\?v=(.{11})", requests.get(req).text)
            link = ("http://www.youtube.com/watch?v=" + searchresults[0])
            url = (link)
            serverinfo[message.guild].Player = await YTDLSource.from_url(link,loop = client.loop)
            serverinfo[message.guild].MusicAuthor = message.author
            while message.guild.voice_client == None:
                await message.guild.voice_client.play(Player)
            serverinfo[message.guild].Player = await YTDLSource.from_url(link,loop = client.loop)
            minutes = int(serverinfo[message.guild].Player.duration/60)
            seconds = int(serverinfo[message.guild].Player.duration-(minutes*60))
            hours = int(minutes/60)
            if hours > 0:
                minutes = minutes-(hours*60)
                if len(str(minutes))==1:
                    minutes="0"+str(minutes)
                if len(str(seconds)) == 1:
                    serverinfo[message.guild].Duration= str(hours)+":"+str(minutes)+":"+"0"+str(seconds)
                else:
                    serverinfo[message.guild].Duration = str(hours)+":"+str(minutes)+":"+str(seconds)
            else:
                if len(str(seconds)) ==1:
                    serverinfo[message.guild].Duration = str(minutes)+":"+"0"+str(seconds)
                else:
                    serverinfo[message.guild].Duration = str(minutes)+":"+str(seconds)
        if serverinfo[message.guild].Player.duration == 0:
            print("CurrentlyLive")
            serverinfo[message.guild].Live = True
        import time
        sec = serverinfo[message.guild].Player.duration
        title = serverinfo[message.guild].Player.title
        em = discord.Embed(title="" , description=("["+ serverinfo[message.guild].Player.title + "]" "("+link+")"+ "\n" + '**' + 'Duration: ' + '**' + '`' + "0:00"  + "/" + str(serverinfo[message.guild].Duration) + "`" +   '\n' + '**' + 'Volume:  '+ '**' + "``" + str(serverinfo[message.guild].Volume) + "%" +  "``" + "\n" + "**" +  "Queue:" + "**" +  "\nNo Songs In Queue" ), colour=3447003)
        em.set_author(name="Selected By: " + str(message.author),icon_url=message.author.avatar_url)
        em.set_footer(text=get_footer())
        serverinfo[message.guild].Music_SOS = await message.channel.send(embed=em)
        serverinfo[message.guild].Minute = 0
        serverinfo[message.guild].second = 0
        serverinfo[message.guild].Hour = 0
        serverinfo[message.guild].background = 0
        serverinfo[message.guild].starttime = datetime.datetime.now()
        serverinfo[message.guild].secondoffset = 0
        message.guild.voice_client.play(serverinfo[message.guild].Player)

        # while serverinfo[message.guild].Second < sec and not (serverinfo[message.guild].Skip or serverinfo[message.guild].LeaveVC):
        #     #print("Hal is stupid")
        #
        #     print(serverinfo[message.guild].Second)
        #     print(sec)
        #
        #     if serverinfo[message.guild].Leave == True:
        #         break
        #     if serverinfo[message.guild].Skip == True:
        #         break
        #     import time
        #     timenow = datetime.datetime.now()
        #     serverinfo[message.guild].Skip = False
        #     second = (timenow - serverinfo[message.guild].starttime).seconds + serverinfo[message.guild].secondoffset
        #     Description = str(serverinfo[message.guild].Progress)
        #     if serverinfo[message.guild].Live == True:
        #         Description = "Currently Live"
        #     if serverinfo[message.guild].Pause == True:
        #         Description = "Paused"
        #     em = discord.Embed(title="" , description=("["+ serverinfo[message.guild].Player.title + "]" "("+link+")"+ "\n" + '**' + 'Duration: ' + '**' + '`'  +  Description + "/" + str(serverinfo[message.guild].Duration) + "`" +   '\n' + '**' + 'Volume:  '+ '**' + "``" + str(serverinfo[message.guild].Volume) + "%" + "``" + "\n"  + "**" + "Queue:" + "**" + str(serverinfo[message.guild].QueueList)), colour=3447003)
        #     em.set_author(name="Selected By: " + str(message.author),icon_url=message.author.avatar_url)
        #     em.set_footer(text=get_footer())
        #     print(Description)
        #     try:
        #         await serverinfo[message.guild].Music_SOS.edit(embed=em)
        #
        #     except discord.errors.NotFound:
        #          serverinfo[message.guild].Music_SOS = await message.channel.send(embed = em)
        #
        #     if serverinfo[message.guild].Leave or serverinfo[message.guild].Skip == True:
        #         break
        #
        #     if serverinfo[message.guild].second == 30:
        #         await serverinfo[message.guild].Music_SOS.delete()
        #         serverinfo[message.guild].Music_SOS = await message.channel.send(embed = em)
        #     if serverinfo[message.guild].Background >= 59:
        #         serverinfo[message.guild].Minute = int(serverinfo[message.guild].Minute)
        #         serverinfo[message.guild].Secondoffset -= 60
        #         serverinfo[message.guild].Minute += 1
        #     if serverinfo[message.guild].Minute == 60:
        #         serverinfo[message.guild].Minute = int(serverinfo[message.guild].Minute)
        #         serverinfo[message.guild].Minute = 0
        #         serverinfo[message.guild].Hour += 1
        #     await asyncio.sleep(1)

        # serverinfo[message.guild].Secondoffset = 0
        # serverinfo[message.guild].Second = 0
        # serverinfo[message.guild].starttime = datetime.datetime.now()
        # timenow = datetime.datetime.now()
        # serverinfo[message.guild].Second = 0
        # print ("Song is done")
        # await serverinfo[message.guild].Music_SOS.delete()
        # serverinfo[message.guild].currentlyplaying = False
        # if len(serverinfo[message.guild].Queue) == 0:
        #     return
        # if len(serverinfo[message.guild].Queue) > 0:
        #     serverinfo[message.guild].Second = 0
        #     serverinfo[message.guild].Secondoffset = 0
        #     serverinfo[message.guild].starttime = datetime.datetime.now()
        #     timenow = datetime.datetime.now()
        #     #serverinfo[message.guild].Second = (timenow - serverinfo[message.guild].starttime).seconds + serverinfo[message.guild].secondoffset
        #     currentlyplaying = True
        #     serverinfo[message.guild].Player = await YTDLSource.from_url(serverinfo[message.guild].Queue[0][1],loop = client.loop)
        #     serverinfo[message.guild].Secondoffset = (datetime.datetime.now() - timenow).seconds
        #     sec = serverinfo[message.guild].Player.data["duration"]
        #     minutes = int(sec/60)
        #     seconds = int(sec-(minutes*60))
        #     hours = int(minutes/60)
        #     if serverinfo[message.guild].Hour > 0:
        #         minutes = minutes-(hours*60)
        #         if len(str(minutes))==1:
        #             minutes="0"+str(minutes)
        #         if len(str(seconds)) == 1:
        #             serverinfo[message.guild].Duration= str(hours)+":"+str(minutes)+":"+"0"+str(seconds)
        #         else:
        #             serverinfo[message.guild].Duration = str(hours)+":"+str(minutes)+":"+str(seconds)
        #     else:
        #         if len(str(seconds)) ==1:
        #             serverinfo[message.guild].Duration = str(minutes)+":"+"0"+str(seconds)
        #         else:
        #             serverinfo[message.guild].Duration = str(minutes)+":"+str(seconds)
        #     serverinfo[message.guild].Queue.remove(serverinfo[message.guild].Queue[0])
        #     serverinfo[message.guild].QueueList = ""
        #     for x in serverinfo[message.guild].Queue:
        #         serverinfo[message.guild].QueueList += "\n" + "["+ x[0][0] + "]" "("+x[1]+")"
        #     if len(serverinfo[message.guild].Queue)<1:
        #         serverinfo[message.guild].QueueList="\nNo Songs In Queue"
        #     message.guild.voice_client.play(serverinfo[message.guild].Player)
        #     serverinfo[message.guild].Skip = False
        #     if serverinfo[message.guild].Live == False:
        #         serverinfo[message.guild].Second = 0
        #         serverinfo[message.guild].Minute = 0
        #     em = discord.Embed(title="" , description=("["+ serverinfo[message.guild].Player.title + "]" "("+link+")"+ "\n" + '**' + 'Duration: ' + '**' + '`'  +  Description + "/" + str(serverinfo[message.guild].Duration) + "`" +   '\n' + '**' + 'Volume:  '+ '**' + "``" + str(serverinfo[message.guild].Volume) + "%" + "``" + "\n"  + "**" + "Queue:" + "**" + str(serverinfo[message.guild].QueueList)), colour=3447003)
        #     em.set_author(name="Selected By: " + str(message.author),icon_url=message.author.avatar_url)
        #     em.set_footer(text=get_footer())
        #     serverinfo[message.guild].Music_SOS = await message.channel.send(embed = em)


async def SKIP(message,serverinfo,client):
    if serverinfo[message.guild].Player == None:
        await message.channel.send("`Hal is not in a voice channel.`")
    if serverinfo[message.guild].Player!=None:
        if message.guild.voice_client.is_playing():
            serverinfo[message.guild].Skip = True
            serverinfo[message.guild].Resume = True
            serverinfo[message.guild].Pause= False
            message.guild.voice_client.stop()
            serverinfo[message.guild].Background = 0
            serverinfo[message.guild].songended = True
            serverinfo[message.guild].secondoffset = 0
        await message.channel.send("`Song Skipped`")

async def LEAVE (message,serverinfo,client):
    if serverinfo[message.guild].Player == None:
            await message.channel.send("`Hal Is Not In A Voice Channel`")
    if serverinfo[message.guild].Player != None:
        print ("Leave")
        serverinfo[message.guild].Leave = True
        serverinfo[message.guild].Skip = True
        serverinfo[message.guild].Queue = []
        serverinfo[message.guild].Resume = True
        serverinfo[message.guild].Pause= False
        await message.guild.voice_client.disconnect()
        #Player = None
        await message.channel.send("`Hal has been disconnected from the voice channel`")

async def PAUSE (message,serverinfo,client):
    if serverinfo[message.guild].Pause == False:
        serverinfo[message.guild].Pause = True
        serverinfo[message.guild].Resume = False
        message.guild.voice_client.pause()
    else:
        await message.channel.send("`Music Already Paused.`")

async def RESUME (message,serverinfo,client):
    if serverinfo[message.guild].Resume == False:
        await message.channel.send("`Music Resumed.`")
        serverinfo[message.guild].Resume = True
        serverinfo[message.guild].Pause= False
        message.guild.voice_client.resume()
    else:
        await message.channel.send("`Music Already Unpaused.`")

async def QUEUE (message,serverinfo,clinet):
    em = discord.Embed(colour = 3447033)
    em = discord.Embed(title= "Queue", description=(serverinfo[message.guild].QueueList), colour=3447003)
    em.set_footer(text=get_footer())
    await message.channel.send(embed = em)

command["*PLAY"] = PLAY
command["*SKIP"] = SKIP
command["*LEAVE"] = LEAVE
command["*PAUSE"] = PAUSE
command["*RESUME"] = RESUME
command["*QUEUE"] = QUEUE

for command_name in command.keys():
  commands.append(command_name)
