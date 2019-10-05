import asyncio
import os
import random
from itertools import cycle

import youtube_dl
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from youtube_dl import *
messages = joined = 0

client = commands.Bot (command_prefix='rtd.',
                       command_description='Hi I am Retard Bot. I give you very un-true information')

status = cycle (['do rtd.help to get started! ps, just do the say command whenever', 'im  a little stupid',
                 'look at my description'])
songs = asyncio.Queue ( )
play_next_song = asyncio.Event ( )

players = {}

math = ['ballsack', 'cracka penis', ]
science = ['wawa bitch im a baby', 'i sit on children', 'i have lou gerigs disease', 'you built like stephen hawking', ]
ss = ['boutta toss this tea bruh', 'THEY ARE IN THE TREES', 'run forrest run!', 'banned from chruch like stalin', ]
ela = [
    'We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defense, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America.',
    'Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.',
    'Iceland is a free and sovereign state, resting on the cornerstones of freedom, equality, democracy and human rights. The government shall work for the welfare of the inhabitants of the country, strengthen their culture and respect the diversity of human life, the land and the biosphere', ]


@client.event
async def on_ready() :
    await client.change_presence (activity=discord.Game ('look at my description!'), status=discord.Status.online)
    change_status.start ( )
    print ('bot is ready')


# moderation commands

@tasks.loop (seconds=10)
async def change_status() :
    await client.change_presence (activity=discord.Game (next (status)))


@client.command ( )
async def kick(ctx, member: discord.Member, *, reason=None) :
    """kicks a member of the discord"""
    await member.kick (reason=reason)


@client.command ( )
async def ban(ctx, member: discord.Member, *, reason=None) :
    """bans a memeber of the discord"""
    await member.ban (reason=reason)
    await ctx.send (f'Banned {member.name, member.discriminator}')


@client.command ( )
async def unban(ctx, *, member) :
    """unbans a banned user of the discord"""
    banned_users = await ctx.guild.bans ( )
    member_name, member_discriminator = member.split ('#')

    for ban_entry in banned_users :
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator) :
            await ctx.guild.unban (user)
            await ctx.send (f'Unbanned {user.name}#{user.discriminator}')


@client.command ( )
async def clear(ctx, amount=10) :
    """clears spam/messages to make space"""
    await ctx.channel.purge (limit=amount)


# music/voice commands
@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


# meme/fun commands to do

@client.command()
async def saymath(ctx) :
    """says a fact not involving math"""
    await ctx.send (random.choice (math))


@client.command()
async def sayscience(ctx) :
    """says a fact not involving science"""
    await ctx.send (random.choice (science))


@client.command()
async def sayela(ctx) :
    """says a fact not involving ela"""
    await ctx.send (random.choice (ela))


@client.command()
async def sayss(ctx) :
    """says a fact not involving social studies"""
    await ctx.send (random.choice (ss))

token = ('NTk5NzM2OTYwNzk3NTA3NjE0.XU18uA.U_weSl0YS1zpEuzzKj-as9DNlVg')
client.run(token)
