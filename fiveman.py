import asyncio
import json
import os

import discord

import db_worker
import fetch
import json_loader
from hots_build_builder import BuildBuilder

CLIENT = discord.Client()
CONFIGS = json_loader.get_json("config.json")
JSON_KEYS = json_loader.get_json("keys.json")
#TEXT_COMMANDS = json_loader.get_json("text_commands.json")
HEROES_JSON = json_loader.get_json("heroes.json")
BUILD_BUILDER = BuildBuilder()

KEY = JSON_KEYS['five-man']
JAWS_VARS = ['JAWSDB_NAME', 'JAWSDB_PASS', 'JAWSDB_HOST', 'JAWSDB_USER']
JAWS_VALS = [os.environ.get(key) for key in JAWS_VARS]
JAWS_DICT = dict(zip(JAWS_VARS, JAWS_VALS))
DB_CONN = db_worker.get_connection(JAWS_DICT)
TEXT_COMMANDS = db_worker.get_text_commands_dict(DB_CONN)

@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('--------')


@CLIENT.event
async def on_message(message):
    if(message.content.startswith("!build")):
        hero = message.content.split()[1]
        print(hero)
        builds = BUILD_BUILDER.get_builds_for_hero(hero)
        await CLIENT.send_message(message.channel, builds)
    if(message.content.startswith("[[")):
        talent = message.content[2:-2].lower()
        description = BUILD_BUILDER.get_talent(talent)
        await CLIENT.send_message(message.channel, description)
    if(message.content.startswith("!addtxtcmd")):
        if(str(message.author) == "kregnax#2710"):
            cmd_in = message.content.split()
            if(cmd_in[0] == "!addtxtcmd"):
                TEXT_COMMANDS[cmd_in[1]] = ''.join(
                    w + ' ' for w in cmd_in[2:]).strip()
                temp_json = json.dumps(TEXT_COMMANDS)
                temp_json = json.loads(temp_json)
                with open('text_commands.json', 'w') as f:
                    json.dump(temp_json, f, indent=4)
            else:
                await CLIENT.send_message(message.channel, "Unrecognized command: {}".format(cmd_in[0]))
        else:
            await CLIENT.send_message(message.channel, "You don't have access, pleb.")
    if(message.content == "?text"):
        commands = 'Available text commands:\n'
        for k, v in TEXT_COMMANDS.items():
            commands += "!{}\n".format(k)
        await CLIENT.send_message(message.channel, commands)
    if(message.content.startswith('!')):
        command = str(message.content).split()[0][1:]
        if(command in TEXT_COMMANDS):
            await CLIENT.send_message(message.channel, TEXT_COMMANDS[command])
    if(message.content.startswith('!strong')):
        hero = message.content.split()[1]
        counters = fetch.get_strong_counters(hero)
        await CLIENT.send_message(message.channel, counters)
    if(message.content.startswith('!weak')):
        hero = message.content.split()[1]
        counters = fetch.get_weak_counters(hero)
        await CLIENT.send_message(message.channel, counters)
    if(message.content.startswith('!patchfor')):
        hero = message.content.split()[1]
        counters = fetch.get_hero_patch_notes(hero)
        await CLIENT.send_message(message.channel, counters)
    if(message.content.startswith('!patchnotes')):
        patch_notes_link = fetch.get_latest_patch_notes()
        patch_notes_link = '3 most recent patches:\n' + patch_notes_link
        await CLIENT.send_message(message.channel, patch_notes_link)

CLIENT.run(KEY)
