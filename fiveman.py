import asyncio
import os

import discord

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


@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('--------')

@CLIENT.event
async def on_message(message):
    if(message.content.startswith("!registertag")):
        discordID = str(message.author)
        battletag = message.content.split()[1]
        db_worker.register_discordID_for_battletag(db_worker.get_connection(JAWS_DICT), discordID, battletag)
    if(message.content.startswith("!build")):
        split_msg = message.content.split()
        command = split_msg[0]
        hero = ''.join(split_msg[1:])
        builds = BUILD_BUILDER.get_builds_for_hero(hero)
        await CLIENT.send_message(message.channel, builds)
    if(message.content.startswith("[[")):
        info_request = message.content[2:-2].lower()
        msg = BUILD_BUILDER.process_request(info_request)
        talent = message.content[2:-2].lower()
        #description = BUILD_BUILDER.get_talent(talent)
        await CLIENT.send_message(message.channel, msg)
    if(message.content.startswith("!addtxtcmd")):
        if(str(message.author) == "kregnax#2710"):
            cmd_in = message.content.split()
            if(cmd_in[0] == "!addtxtcmd"):
                text_command = cmd_in[1]
                text_output = ''.join(w + ' ' for w in cmd_in[2:]).strip()
                TEXT_COMMANDS[text_command] = text_output
                db_worker.add_new_text_command(db_worker.get_connection(JAWS_DICT), text_command, text_output)
            else:
                await CLIENT.send_message(message.channel, "Unrecognized command: {}".format(cmd_in[0]))
        else:
            await CLIENT.send_message(message.channel, "You don't have access, fool.")
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
