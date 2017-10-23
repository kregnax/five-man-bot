import discord
import asyncio
from bs4 import BeautifulSoup
import urllib.request
import random
import re
import sys
import os
import json
import json_loader
import fetch
import requests
import time
from hots_build_builder import BuildBuilder

client = discord.Client()
configs = json_loader.get_json("config.json")
text_commands = json_loader.get_json("text_commands.json")
heroes_json = json_loader.get_json("heroes.json")
build_builder = BuildBuilder()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')

@client.event
async def on_message(message):
    #TODO: use message.attachments to save images with text command
    if(message.content.startswith("$test")):
        if('lost vikings' in heroes_json['tlv']['alias']['misc']):
            await client.send_message(message.channel,heroes_json['tlv']['alias']['hots-cntr'])
    if(message.content.startswith("!build")):
        hero = message.content.split()[1]
        print(hero)
        builds = build_builder.get_builds_for_hero(hero)
        await client.send_message(message.channel, builds)
    if(message.content.startswith("[[")):
        talent = message.content[2:-2].lower()
        description = build_builder.get_talent(talent)
        await client.send_message(message.channel, description)
    if(message.content.startswith("!addtxtcmd")):
        if(str(message.author) == "kregnax#2710"):
            cmd_in = message.content.split()
            if(cmd_in[0] == "!addtxtcmd"):
                text_commands[cmd_in[1]] = ''.join(w+' ' for w in cmd_in[2:]).strip()
                temp_json = json.dumps(text_commands)
                temp_json = json.loads(temp_json)
                with open('text_commands.json','w') as f:
                    json.dump(temp_json, f,indent=4)
            else:
                await client.send_message(message.channel, "Unrecognized command: {}".format(cmd_in[0]))
        else:
            await client.send_message(message.channel, "You don't have access, pleb.")
    if(message.content == "?text"):
        commands = 'Available text commands:\n';
        for k, v in text_commands.items():
            commands += "!{}\n".format(k)
        await client.send_message(message.channel, commands)
    if(message.content.startswith('!')):
        command = str(message.content).split()[0][1:]
        if(command in text_commands):
            await client.send_message(message.channel, text_commands[command])
    if(message.content.startswith('!strong')):
        hero = message.content.split()[1]
        counters = fetch.get_strong_counters(hero)
        await client.send_message(message.channel, counters)
    if(message.content.startswith('!weak')):
        hero = message.content.split()[1]
        counters = fetch.get_weak_counters(hero)
        await client.send_message(message.channel, counters)
    if(message.content.startswith('!patchfor')):
        hero = message.content.split()[1]
        counters = fetch.get_hero_patch_notes(hero)
        await client.send_message(message.channel, counters)
    if(message.content.startswith('!patchnotes')):
        patch_notes_link = fetch.get_latest_patch_notes()
        patch_notes_link = '3 most recent patches:\n'+patch_notes_link
        await client.send_message(message.channel, patch_notes_link)
client.run('MzYzMTEzNDY0NTg0OTk0ODE4.DLMxNA.K-z0tleRpvrNykggsmUP5VZ56SI')