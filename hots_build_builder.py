import json
import json_loader
import fetch

class BuildBuilder(object):

    VALID_LEVELS = [1, 4, 7, 10, 13, 16, 20]

    def __init__(self):
        self.content_lookup = json_loader.get_json("content_lookup.json")
        #TODO: break this out into smaller functions so selection of
        #       builds can be more granular, i.e. create a
        #       get_build_by_name()

    def process_request(self, request):
        if '/' in request:
            sliced = request.split('/')
            hero = sliced[0]
            affix = sliced[1]
            try:
                level = int(affix)
                return self.get_talents_for_level(hero, level)
            except:
                return 'Lookup by [[hero/talent]] not implemented'
        else:
            return self.get_talent(request)
        return 'Not a valid request: ' + request

    def get_builds_for_hero(self, hero):
        '''Uses content_lookup and hotsapi to return formatted builds for a hero'''
        hero_name = fetch.get_hero_name(hero)
        if hero_name == 'Not a valid hero':
            return hero_name
        #Get an array of dicts with hero talents
        hero_talents = fetch.get_hero_talents(hero_name)
        final_build = 'Builds for {hero}:\n'.format(hero=hero_name)
        builds = self.content_lookup[hero_name]["builds"]
        #Iterate through the builds to get talent names at each level
        for build_name, talent_choices in builds.items():
            final_build += '__{build_name}__\n'.format(build_name=build_name)
            for i, choice in enumerate(talent_choices):
                level = self.VALID_LEVELS[i]
                try:
                    talent_title = (talent['title'] for talent in hero_talents if talent['level']==level and talent['sort']==choice).__next__()
                except StopIteration as e:
                    talent_title = 'Talent not found for Level {level} and Sort {sort}.'.format(level=level, sort=choice)
                final_build += '\t{level} : {talent_title}\n'.format(level=level, talent_title=talent_title)
        return final_build

    def get_talents_for_hero(self, hero):
        hero_name = fetch.get_hero_name(hero)
        if hero_name == 'Not a valid hero':
            return hero_name
        final_talents = 'Talents for {}:\n'.format(hero_name)
        talents = self.heroes_json[hero]["talents"]
        for talent in talents:
            continue

    def get_talent(self, talent):
        found_talent = ''
        for hero in self.heroes_json:
            talents = self.heroes_json[hero]["talents"]
            for t in talents:
                if t["name"].lower() == talent:
                    hero = hero[0].upper() + hero[1:]
                    found_talent += '__{}__: {} - {}\n\n'.format(hero,t["name"],t["description"])
        if found_talent == '':
            return 'Could not find info for talent __{}__'.format(talent)
        return found_talent

    def get_talents_for_level(self, hero, level):
        if level not in self.VALID_LEVELS:
            return level + ' is not a valid level'
        hero_name = fetch.get_hero_name(hero)
        if hero_name == 'Not a valid hero':
            return hero_name
        talent_list = ''
        hero_talents = fetch.get_hero_talents(hero_name)
        
        for t in hero_talents:
            if level == t['level']:
                talent_list += '__{}__: {}\n\n'.format(t['title'],t['description'])
        return talent_list

    #TODO: get talents by name, maybe use string comparison with 85%
    #       threshhold of name to return relevant talents (see reddit bot)