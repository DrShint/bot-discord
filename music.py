import discord
from discord.ext import commands
import youtube_dl
from time import sleep

from youtube_dl import YoutubeDL


class music(commands.Cog):
    def __unit__(self, client):
        self.client = client

        self.is_playing = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            print(self.music_queue)
            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            await self.vc.disconnect()

    @commands.command()
    async def ajuda(self, ctx):
        await ctx.send('**!join - Juntar-se a sua sala\n!play - Insira o comando com um link do YouTube para ouvir\n!pause - Pausar\n!resume - Retornar do pause\n!disconnect - Disconectar o BOT**')


    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('Você não está em um canal de voz!')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send( 'Iae meu bom, tranquilo?')
            sleep(1)
            await ctx.send('O que vocês querem ouvir?')
            sleep(2)
            await ctx.send('Ah, já ia me esquecendo... Se precisar de ajuda, só digitar **!ajuda**')
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.send('Se quiser ouvir música de novo, é só chamar!!')
        sleep(1)
        await ctx.send('BOT feito por: **𝔻𝕣.𝕊𝕙𝕚𝕟𝕥.**')
        await ctx.voice_client.disconnect()

    @commands.command(name="play", help="Toca uma música do YouTube", aliases=['p', 'tocar'])
    async def p(self, ctx, embedvc=None, *args):
        query = " ".join(args)

        try:
            voice_channel = ctx.author.voice.channel
        except:
            # if voice_channel is None:
            # you need to be connected so that the bot knows where to go
            embedvc = discord.Embed(
                colour=1646116,  # grey
                description='Para tocar uma música, primeiro se conecte a um canal de voz.'
            )
            await ctx.send(embed=embedvc)
            return
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                vc = discord.Embed(
                    colour=12255232,  # red
                    description='Algo deu errado! Tente mudar ou configurar a playlist/vídeo ou escrever o nome dele novamente!'
                )
                await ctx.send(embed=embedvc)
            else:
                embedvc = discord.Embed(
                    colour=32768,  # green
                    description=f"Você adicionou a música **{song['title']}** à fila!\n\n[Crie seu próprio Bot de Música](https://youtu.be/YGx0xNHzjgE)"
                )
                await ctx.send(embed=embedvc)
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def pause(self, ctx):
        await ctx.send('Paused ⏸')
        await ctx.voice_client.pause()


    @commands.command()
    async def resume(self, ctx):
        await ctx.send('Resume ▶')
        await ctx.voice_client.resume()



def setup(client):
    client.add_cog(music(client))
