import discord
from discord.ext import commands
import youtube_dl
import random
class music(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.queues=[]
        self.queuename=[]
    def check_queue(self,ctx):
        if (~ctx.voice_client.is_playing()):
            if self.queues!=[]:
                ch=self.queuename.pop(0)
                source=self.queues.pop(0)
                vc = ctx.voice_client
                msg="Now playing : `"+ch+"`"
                embed=discord.Embed(title=msg, description=f"[{ctx.message.author.mention}]", color=0xb30000)
                embed.set_thumbnail(url="https://i.imgur.com/vxEF9YX.png")
                self.client.loop.create_task(ctx.send(embed=embed))
                vc.play(source,after=lambda x=None: self.check_queue(ctx))
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'My ping is {round(self.client.latency* 1000)} ms!')
    @commands.command()
    async def purge(self,ctx):
        self.queue=[]
        self.queuename=[]
        await ctx.send('I have purged the queue successfully')
    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        Voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await Voice_channel.connect()
        else:
            await ctx.voice_client.move_to(Voice_channel)
        self.check_queue(ctx)
    @commands.command(aliases=['dc', 'leave' ,'quit'])
    async def disconnect(self,ctx):
        await ctx.voice_client.disconnect(force=True)
    @commands.command(aliases=['s'])
    async def skip(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        ctx.voice_client.pause()
        self.check_queue(ctx)
    @commands.command(aliases=['pau', 'stop'])
    async def pause(self,ctx):
        ctx.voice_client.pause()
        await ctx.send("paused")
    
    @commands.command(aliases=['r', 'resuming'])
    async def resume(self,ctx):
        ctx.voice_client.resume()
        await ctx.send("resumed")

    @commands.command(aliases=['p', 'playing'])
    async def play(self,ctx,*args):
        url=' '.join(args)
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        Voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await Voice_channel.connect()
        else:
            await ctx.voice_client.move_to(Voice_channel)
        if ctx.voice_client.is_playing():
            await self.queue(ctx,url)
        else :
            ctx.voice_client.stop()
            FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                'options':'-vn'}
            YDL_OPTIONS={'format':"bestaudio",
                        'default_search': 'auto'}
            vc = ctx.voice_client
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    for i in info['entries']:
                        video_format = i["formats"][0]
                        title = i['title']
                        url2 = video_format['url']
                        source = await discord.FFmpegOpusAudio.from_probe(url2,
                        **FFMPEG_OPTIONS)
                        if(i==info['entries'][0]):
                                sourceFirst=source
                                titleFirst=title
                                msg="Now playing : `"+titleFirst+"`"
                                embed=discord.Embed(title=msg, description=f"[{ctx.message.author.mention}]", color=0xb30000)
                                embed.set_thumbnail(url="https://i.imgur.com/vxEF9YX.png")
                                await ctx.send(embed = embed)
                                vc.play(sourceFirst, after=lambda x=None: self.check_queue(ctx))
                        elif(len(info['entries'])>1):
                            self.queues.append(source)
                            self.queuename.append(title)
                    if (len(info['entries'])>1):
                        await ctx.send(f"Added `{len(info['entries'])}` element To Queue !")
                elif 'formats' in info:
                    video_format = info["formats"][0]
                    titleFirst = info.get('title', None)
                    url2 = video_format['url']
                    sourceFirst = await discord.FFmpegOpusAudio.from_probe(url2,
                    **FFMPEG_OPTIONS)
                    msg="Now playing : `"+titleFirst+"`"
                    embed=discord.Embed(title=msg, description=f"[{ctx.message.author.mention}]", color=0xb30000)
                    embed.set_thumbnail(url="https://i.imgur.com/vxEF9YX.png")
                    await ctx.send(embed = embed)
                    vc.play(sourceFirst, after=lambda x=None: self.check_queue(ctx))
    @commands.command(aliases=['cf', 'coin'])
    async def coinflip(self,ctx):
        x=random.randint(0, 1)
        c=["Heads","Tails"]
        await ctx.send(f'> {c[x]}')
    @commands.command(aliases=['clr', 'cl'])
    async def clear(self,ctx, number):
        number=int(number)
        await ctx.channel.purge(limit=number)
        await ctx.send(f"> I've successfully purged {number} messages !")
    def view_queue(self):
        embed=discord.Embed(title="Queue", description=" ", color=0xb30000)
        embed.set_thumbnail(url="https://cdn.iconscout.com/icon/free/png-256/queue-music-1779820-1513985.png")
        if(self.queuename!=[]):
            msg=""
            i=1
            for item in self.queuename:
                msg=f'{i} : {item} \n'
                embed.add_field(name=msg, value='\u200b' , inline=False)
                i+=1
            return embed
        embed.description="The queue is empty  :dash:"
        return embed
    @commands.command(aliases=['q'])
    async def queue(self,ctx,url=None):
         if(url is None):
            embed=self.view_queue()
            await ctx.send(embed=embed)
         else:
            if ctx.author.voice is None:
                await ctx.send("You're not in a voice channel")
            Voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await Voice_channel.connect()
            else:
                await ctx.voice_client.move_to(Voice_channel)
            FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                'options':'-vn'}
            YDL_OPTIONS={'format':"bestaudio",
                        'default_search': 'auto'}
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    for i in info['entries']:
                        video_format = i["formats"][0]
                        title = i['title']
                        url2 = video_format['url']
                        source = await discord.FFmpegOpusAudio.from_probe(url2,
                        **FFMPEG_OPTIONS)
                        self.queues.append(source)
                        self.queuename.append(title)
                    if(len(info['entries'])>1):
                        await ctx.send(f"Added `{len(info['entries'])}` elements To Queue !")
                    else:
                        await ctx.send(f"Added `{title}` to Queue !")
                elif 'formats' in info:
                    video_format = info["formats"][0]
                    title = info.get('title', None)
                    url2 = video_format['url']
                    source = await discord.FFmpegOpusAudio.from_probe(url2,
                    **FFMPEG_OPTIONS)
                    self.queues.append(source)
                    self.queuename.append(title)
                    await ctx.send(f"Added `{title}` To Queue !")
    @commands.command()
    async def avatar(self, ctx, *,  avamember : discord.Member=None):
        userAvatarUrl = avamember.avatar_url
        await ctx.send(userAvatarUrl)
    
def setup(client):
    client.add_cog(music(client))