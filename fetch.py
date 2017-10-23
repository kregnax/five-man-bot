from bs4 import BeautifulSoup
import requests
import re
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_latest_patch_notes():
    links = []
    url = 'https://heroespatchnotes.com/patch/'
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    for a in soup.findAll('a', attrs={'class':'official'}, limit=3):
        links.append(a.get('href'))
    link_string = '\n'.join(links)
    return link_string

#def get_hero_list():
#    '''Returns a list of current heroes from battlenet'''
#    url = "http://us.battle.net/heroes/en/heroes/#/"
#    page = requests.get(url, verify=False)
#    soup = BeautifulSoup(page.text, 'html.parser')
#    for cd in soup.findAll(text=True):
#        if "window.heroes" in cd:
#            cd = cd.split(".heroes = ")[1]
#            heroes = cd.split(";\n")[0]
#            continue
#    hero_json = json.loads(heroes)
#    hero_list = []
#    for elem in hero_json:
#         hero_list.append(elem['analyticsName'])
#    return hero_list

def get_hero_aliases():
    '''Loops through heroes.json and returns a list of all heroes' aliases ex:hero in get_hero_aliases()'''
    data = json_loader.get_json("heroes.json")
    hero_aliases = []
    for elem in data.keys():
        hero_aliases.append(elem)
        for el in data[elem]['alias']:
            if isinstance(data[elem]['alias'].get(el), list):
                for e in data[elem]['alias'].get(el):
                    hero_aliases.append(e)
            else:
                hero_aliases.append(data[elem]['alias'].get(el))
    return hero_aliases

def get_hero_patch_notes(hero, next_cmd=False):
    '''Input a hero name and return a scraped list of the last change notes for that hero. Might add next note funcaitonality'''
    if hero.lower() in get_hero_aliases():
        url = "https://heroespatchnotes.com/hero/{}.html".format(hero) #abathur.html#patch2017-09-26"
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        notes_list = []
        for elem in soup.find("div", class_="panel panel-primary").find_all("li"):
            notes_list.append(elem.get_text())
    else:
        return "Not a valid hero"
    return '\n'.join(notes_list)

def get_weak_counters(hero):
    if hero.lower() in get_hero_aliases():
        url = 'https://www.heroescounters.com/hero/{}'.format(hero)
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        #soup.title.string
        popularBuild = soup.find('ul',class_='counterlist counterlist-bad')
        count = 0
        hero_counter_list = []
        for link in popularBuild.findAll('a'):
            count+=1
            if count %2 == 0 and count < 11:
                hero_counter_list.append(link.string)
    else:
        return "Not a valid hero"
    return '\n'.join(hero_counter_list)

def get_strong_counters(hero):
    if hero.lower() in get_hero_aliases():
        url = 'https://www.heroescounters.com/hero/{}'.format(hero)
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        #soup.title.string
        popularBuild = soup.find('ul',class_='counterlist counterlist-good')
        count = 0
        hero_counter_list = []
        for link in popularBuild.findAll('a'):
            count+=1
            if count %2 == 0 and count < 11:
                hero_counter_list.append(link.string)
    else:
        return "Not a valid hero"
    return '\n'.join(hero_counter_list)

def test_print_all():
    print(get_strong_counters('tracer'))
    print(get_weak_counters('tracer'))
    print(get_hero_patch_notes('tracer'))
    print(get_hero_list())
