import json

voice_command_json_path = "voice_commands.json"
text_command_json_path = "text_commands.json"

def get_text_commands_json():
    with open(text_command_json_path) as json_file:
        return json.load(json_file)

def get_voice_commands_json():
    with open(voice_command_json_path) as json_file:
        return json.load(json_file)

def get_json(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)