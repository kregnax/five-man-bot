from os import environ

import requests

import db_worker

KEY = environ.get('BLIZZ_KEY')
LOCATION = 'en_US'

career_URL = 'https://us.api.battle.net/d3/profile/{}/'
hero_URL = career_URL + 'hero/{}'
item_URL = 'https://us.api.battle.net/d3/data/item/{}'
payload = {'locale':'en_US','apikey':KEY}

def format_tag_for_api(battletag):
    return battletag.replace('#', '-')

def get_d3_career(battletag):
    battletag = format_tag_for_api(battletag)
    r = requests.get(career_URL.format(battletag), params=payload)
    career = r.json()
    return career