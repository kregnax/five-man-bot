from bs4 import BeautifulSoup
import requests
import json_loader
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GET_ALL_HEROES_URL = 'http://hotsapi.net/api/v1/heroes'
GET_HERO_DETAILS_URL = 'http://hotsapi.net/api/v1/heroes/{hero}'
GET_TALENT_URL = 'http://hotsapi.net/api/v1/talents/{talent}'
GET_ABILITY_URL = 'http://hotsapi.net/api/v1/heroes/{hero}/abilities/{hotkey}'

def get_all_heroes():
    '''Return complete hero info from hotsapi'''
    return requests.get(GET_ALL_HEROES_URL).json()

def get_hero_details(hero):
    '''Return hero details including talents and abilities'''
    return requests.get(GET_HERO_DETAILS_URL.format(hero=hero)).json()

def get_hero_talents(hero):
    '''Returns just the talents for a hero'''
    details = requests.get(GET_HERO_DETAILS_URL.format(hero=hero)).json()
    return details['talents']

def get_talent_info(talent):
    '''Return talent details'''
    return requests.get(GET_TALENT_URL.format(talent=talent)).json()

def get_hero_ability_for_hotkey(hero, hotkey):
    return requests.get(GET_ABILITY_URL.format(hero=hero, hotkey=hotkey)).json()

def get_hero_name(hero):
    '''Return correct hero name when given alias name'''
    alias_json = json_loader.get_json("alias_lookup.json")
    if alias_json.get(hero.lower(), "HeroError") == "HeroError":
        return "Not a valid hero"
    else:
        return alias_json.get(hero.lower())

def get_hero_content_name(hero, content):
    '''Returns correct hero name when given hero name and content type'''
    content_json = json_loader.get_json("content_lookup.json")
    if hero.lower() == get_hero_name(hero.lower()):
        hero_name = content_json.get(hero.lower())[content]
    else:
        return "Not a valid hero"
    return hero_name

def get_latest_patch_notes():
    '''Fetches the last 3 patch notes links'''
    links = []
    url = 'https://heroespatchnotes.com/patch/'
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    for sp_ref in soup.findAll('a', attrs={'class':'official'}, limit=3):
        links.append(sp_ref.get('href'))
    link_string = '\n'.join(links)
    return link_string

def get_hero_patch_notes(hero):
    '''Fetches scraped list of the last change notes for given hero'''
    if hero.lower() in get_hero_name(hero.lower()):
        hero = get_hero_content_name(hero.lower(), "hots-pch-nts")
        url = "https://heroespatchnotes.com/hero/{}.html".format(hero)
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        notes_list = []
        for elem in soup.find("div", class_="panel-body table-responsive").find_all("li"):
            notes_list.append(elem.get_text().replace("\n\n", "\n"))
    else:
        return "Not a valid hero"
    return '\n'.join(notes_list)

def get_weak_counters(hero):
    '''Fetches counters that a hero is weak against'''
    if hero.lower() in get_hero_name(hero.lower()):
        hero = get_hero_content_name(hero.lower(), "hots-cntr")
        url = 'https://www.heroescounters.com/hero/{}'.format(hero)
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        counter_list = soup.find('ul', class_='counterlist counterlist-bad')
        count = 0
        hero_counter_list = []
        for link in counter_list.findAll('a'):
            count += 1
            if count %2 == 0 and count < 11:
                hero_counter_list.append(link.string)
    else:
        return "Not a valid hero"
    return '\n'.join(hero_counter_list)


def get_strong_counters(hero):
    '''Fetches counters that a hero is strong against'''
    if hero.lower() in get_hero_name(hero.lower()):
        hero = get_hero_content_name(hero.lower(), "hots-cntr")
        url = 'https://www.heroescounters.com/hero/{}'.format(hero)
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        counter_list = soup.find('ul', class_='counterlist counterlist-good')
        count = 0
        hero_counter_list = []
        for link in counter_list.findAll('a'):
            count += 1
            if count %2 == 0 and count < 11:
                hero_counter_list.append(link.string)
    else:
        return "Not a valid hero"
    return '\n'.join(hero_counter_list)

def test_print_all():
    '''test all the things'''
    print(get_strong_counters('the lost vikings'))
    print(get_weak_counters('the lost vikings'))
    print(get_hero_patch_notes('the lost vikings'))
