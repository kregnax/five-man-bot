import asyncio
import os
import discord
import fetch
from discord.ext import commands

CLIENT = discord.Client()

bot = commands.Bot(command_prefix="!", description="Testing this thing")


@bot.event
async def on_ready():
    print("Logged in")


@bot.command()
async def say(ctx):
    print("called say")
    await ctx.send("say it to my FACE")


@bot.command()
async def strong(ctx):
    await ctx.send('Go away, this doesn\'t work yet')


@bot.command()
async def weak(ctx):
    await ctx.send('Go away, this doesn\'t work yet')


@bot.command()
async def patchfor(ctx):
    await ctx.send('Go away, this doesn\'t work yet')


@bot.command()
async def build(ctx):
    await ctx.send('Go away, this doesn\'t work yet')


@bot.command()
async def patchnotes(ctx):
    '''Shows the 3 most recent patches.'''
    patch_notes_links = fetch.get_latest_patch_notes()
    patch_notes_links = '3 most recent patches:\n' + patch_notes_links
    await ctx.send(patch_notes_links)


bot.run(os.environ.get('FIVE_MAN_BOT_KEY'))
