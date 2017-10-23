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
from voice_manager import VoiceManager
from hots_build_builder import BuildBuilder

client = discord.Client()
configs = json_loader.get_json("config.json")
text_commands = json_loader.get_json("text_commands.json")
heroes_json = json_loader.get_json("heroes.json")
voice_files_location = configs["voice"]["directory_name"]
voice_manager = VoiceManager(client, voice_files_location)
voice_commands = voice_manager.get_voice_commands()
build_builder = BuildBuilder()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')
    #print(fetch.test_print_all())
    if sys.maxsize > 2**32:
        discord.opus.load_opus('libopus-0.x64.dll')
    else:
        discord.opus.load_opus('libopus-0.x86.dll')

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
    if(message.content.startswith("!voice")):
        await voice_manager.add_to_queue(message)
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
    if(message.content == "?voice"):
        commands = voice_manager.get_voice_command_help()
        await client.send_message(message.channel, commands)
    if(message.content.startswith('!')):
        #await client.delete_message(message)
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
    if(message.content.startswith('!garbagewater')):
        await voice_manager.play_audio(message, '.voice_lines/special/garbagewater.mp3', .15)
    if(message.content.startswith('!momma')):
        url = 'https://biffthecamel.herokuapp.com/yomomma'
        r = requests.get(url)
        joke = r.text
        input_text = ' '.join(message.content.split()[1:])
        rq = requests.get('https://biffthecamel.herokuapp.com/tts?t={}'.format(joke), stream=True)
        local_file_path = '.temp/{}.mp3'.format(int(time.time()))
        with open(local_file_path, 'wb') as f:
            for chunk in rq.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
            f.close()
        await voice_manager.add_to_queue(message, local_file_path)
    if(message.content.startswith('!tts')):
        input_text = ' '.join(message.content.split()[1:])
        r = requests.get('https://biffthecamel.herokuapp.com/tts?t={}'.format(input_text), stream=True)
        local_file_path = '.temp/{}.mp3'.format(int(time.time()))
        with open(local_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.close()
        await voice_manager.add_to_queue(message, local_file_path)
client.loop.create_task(voice_manager.consume_queue())
client.run('MzYzMTEzNDY0NTg0OTk0ODE4.DLMxNA.K-z0tleRpvrNykggsmUP5VZ56SI')