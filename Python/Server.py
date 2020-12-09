from EssentialPackages import *
from Footer import get_footer
from Music import YTDLSource
import asyncio

class Server:
    def __init__(self,server):
        self.Task = None
        self.Player = None
        self.MusicAuthor = None
        self.MusicTextChannel = None
        self.Skip = False
        self.LeaveVC = False
        self.Pause = False
        self.Resume = False
        self.currentlyplaying = False
        self.Queue = []
        self.Volume = 100
        self.Live = False
        self.Progress = ""
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        self.Secondoffset = 0
        self.Seconds = 0
        self.Background = 0
        self.Duration = ""
        self.QueueList = ""
        self.Music_SOS = None
        self.server = server
        self.music_task = None
        self.everyoneleft = False
        self.end_time = datetime.datetime.now()
        self.starttime = datetime.datetime.now()
        self.loading = False
        self.mHandler = None
        self.server=server
        self.SongEndedTime=datetime.datetime.now()
        self.LeaveMSG=None

    async def update_loop(self):
        print ("Hal Activated...")
        while True:
            if self.currentlyplaying and self.Player != None and self.Music_SOS != None:
                timenow = datetime.datetime.now()
                self.SongEndedTime=datetime.datetime.now()
                self.Background = (timenow - self.starttime).seconds + self.Secondoffset
                self.Second = (timenow - self.starttime).seconds
                self.Minute = int(self.Minute)-(self.Hour*60)
                self.Hour = int(self.Minute/60)
                if self.Hour > 0:
                    self.Minute = self.Minute-(self.Hour*60)
                    if len(str(self.Minute))==1:
                        self.Minute="0"+str(self.Minute)
                    if len(str(self.Background)) == 1:
                        self.Progress= str(self.Hour)+":"+str(self.Minute)+":"+"0"+str(self.Background)
                    else:
                        self.Progress = str(self.Hour)+":"+str(self.Minutes)+":"+str(self.Background)
                else:
                    if len(str(self.Background)) ==1:
                        self.Progress = str(self.Minute)+":"+"0"+str(self.Background)
                    else:
                        self.Progress = str(self.Minute)+":"+str(self.Background)
                import time
                timenow = datetime.datetime.now()
                second = (timenow - self.starttime).seconds + self.Secondoffset
                Description = str(self.Progress) + "/" + str(self.Duration)
                if self.Live == True:
                    Description = "Currently Live"
                if self.Pause == True:
                    Description = "Paused"
                em = discord.Embed(title="" , description=("["+ self.Player.title + "]" "("+self.Player.url+")"+ "\n" + '**' + 'Duration: ' + '**' + '`'  +  Description  + "`" +   '\n' + '**' + 'Volume:  '+ '**' + "``" + str(self.Volume) + "%" + "``" + "\n"  + "**" + "Queue:" + "**" + str(self.QueueList)), colour=3447003)
                em.set_author(name="Selected By: " + str(self.MusicAuthor),icon_url=self.MusicAuthor.avatar_url)
                em.set_footer(text=get_footer())
                try:
                    await self.Music_SOS.edit(embed=em)
                except discord.errors.NotFound:
                     self.Music_SOS = await self.MusicTextChannel.send(embed = em)
                if self.Second%60 == 30:
                    await self.Music_SOS.delete()
                    self.Music_SOS = await self.MusicTextChannel.send(embed = em)
                if self.Background >= 59:
                    self.Minute = int(self.Minute)
                    self.Secondoffset -= 60
                    self.Minute += 1
                if self.Minute == 60:
                    self.Minute = int(self.Minute)
                    self.Minute = 0
                    self.Hour += 1
                if self.Player.duration == 0:
                    self.Live = True
                if self.LeaveVC or self.Skip or (self.Second >= self.Player.duration and not self.Live):
                    self.currentlyplaying=False
                    self.Live = False
                    self.LeaveVC = False
                    self.Player = None
                    self.SongEndedTime = datetime.datetime.now()
                    print("Song ended")
                    self.Secondoffset = 0
                    self.Second = 0
                    self.Skip = False
                    self.starttime = datetime.datetime.now()
                    timenow = datetime.datetime.now()
                    await self.Music_SOS.delete()
                    self.Music_SOS = None
                    if len(self.Queue) > 0:
                        print("Song in queue")
                        self.Second = 0
                        self.Secondoffset = 0
                        self.starttime = datetime.datetime.now()
                        timenow = datetime.datetime.now()
                        #self.Second = (timenow - self.starttime).seconds + self.secondoffset
                        self.currentlyplaying = True
                        self.Player = await YTDLSource.from_url(self.Queue[0][1],loop = asyncio.get_event_loop())
                        self.Secondoffset = (datetime.datetime.now() - timenow).seconds
                        sec = self.Player.data["duration"]
                        minutes = int(sec/60)
                        seconds = int(sec-(minutes*60))
                        hours = int(minutes/60)
                        if self.Hour > 0:
                            minutes = minutes-(hours*60)
                            if len(str(minutes))==1:
                                minutes="0"+str(minutes)
                            if len(str(seconds)) == 1:
                                self.Duration= str(hours)+":"+str(minutes)+":"+"0"+str(seconds)
                            else:
                                self.Duration = str(hours)+":"+str(minutes)+":"+str(seconds)
                        else:
                            if len(str(seconds)) ==1:
                                self.Duration = str(minutes)+":"+"0"+str(seconds)
                            else:
                                self.Duration = str(minutes)+":"+str(seconds)
                        self.Queue.remove(self.Queue[0])
                        self.QueueList = ""
                        for x in self.Queue:
                            self.QueueList += "\n" + "["+ x[0][0] + "]" "("+x[1]+")"
                        if len(self.Queue)<1:
                            self.QueueList="\nNo Songs In Queue"
                        self.server.voice_client.play(self.Player)
                        self.Skip = False
                        if self.Live == False:
                            self.Second = 0
                            self.Minute = 0
                        em = discord.Embed(title="" , description=("["+ self.Player.title + "]" "("+self.Player.url+")"+ "\n" + '**' + 'Duration: ' + '**' + '`'  +  Description + "/" + str(self.Duration) + "`" +   '\n' + '**' + 'Volume:  '+ '**' + "``" + str(self.Volume) + "%" + "``" + "\n"  + "**" + "Queue:" + "**" + str(self.QueueList)), colour=3447003)
                        em.set_author(name="Selected By: " + str(self.MusicAuthor),icon_url=self.MusicAuthor.avatar_url)
                        em.set_footer(text=get_footer())
                        self.Music_SOS = await self.MusicTextChannel.send(embed = em)
            else:
                if (datetime.datetime.now() - self.SongEndedTime).seconds >= 15 and self.LeaveMSG == None:
                    await self.server.voice_client.disconnect()
                    #self.LeaveMSG = await self.MusicTextChannel.send("`Hal has left the voice channel`")
                #if (datetime.datetime.now() - self.SongEndedTime).seconds >= 30 and self.LeaveMSG != None:
                #    await self.LeaveMSG.delete()
                #    self.LeaveMSG=None
            await asyncio.sleep(1)
