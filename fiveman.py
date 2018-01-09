import asyncio
import os

import discord
from discord.ext import commands
import blizzard
import db_worker
import fetch
import json_loader
from hots_build_builder import BuildBuilder


CLIENT = discord.Client()
BUILD_BUILDER = BuildBuilder()
KEY = os.environ.get('FIVE_MAN')#JSON_KEYS['five-man']
JAWS_VARS = ['JAWSDB_NAME', 'JAWSDB_PASS', 'JAWSDB_HOST', 'JAWSDB_USER']
JAWS_VALS = [os.environ.get(key) for key in JAWS_VARS]
JAWS_DICT = dict(zip(JAWS_VARS, JAWS_VALS))
TEXT_COMMANDS = db_worker.get_text_commands_dict(db_worker.get_connection(JAWS_DICT))


bot = commands.Bot(command_prefix="!", description=DESCRIPTION)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="!help"))

@bot.event
async def on_message(message):
    if message.content.startswith("{{") and message.content.endswith("}}"):
        info_request = message.content.strip("[[").strip("]]").lower()
        msg = BUILD_BUILDER.process_request(info_request)
        #talent = message[2:-2].lower()
        #description = BUILD_BUILDER.get_talent(talent)
        await bot.send_message(message.channel, msg)
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def say(ctx, *, message=None):
    if message is None:
        await bot.say("Say something, I'm giving up on you.\nI'll be the bot, if you want me to.")
    else:
        await bot.say(message)

@bot.command(pass_context=True)
async def strong(ctx, *, message=None):
    if message is None:
        await bot.say("What hero counter are you looking for?")
    else:
        counters = fetch.get_strong_counters(message)
        await bot.say(counters)

@bot.command(pass_context=True)
async def weak(ctx, *, message=None):
    if message is None:
        await bot.say("What hero counter are you looking for?")
    else:
        counters = fetch.get_weak_counters(message)
        await bot.say(counters)

@bot.command(pass_context=True)
async def patchfor(ctx, *, message=None):
    if message is None:
        await bot.say("What hero patchnotes are you looking for?")
    else:
        patch = fetch.get_hero_patch_notes(message)
        await bot.say(patch)

@bot.command(pass_context=True)
async def build(ctx, *, message=None, aliases=["build", "builds"]):
    if message is None:
        await bot.say("What hero build are you looking for?")
    else:
        hero = message
        builds = BUILD_BUILDER.get_builds_for_hero(hero)
        await bot.say(builds)

@bot.command()
async def patchnotes():
    patch_notes_links = fetch.get_latest_patch_notes()
    patch_notes_links = '3 most recent patches:\n' + patch_notes_links
    await  bot.say(patch_notes_links)


bot.run(KEY)

