import json
import json_loader
import fetch

class BuildBuilder(object):

    VALID_LEVELS = [1, 4, 7, 10, 13, 16, 20]

    def __init__(self):
        self.heroes_json = json_loader.get_json("heroes.json")
        self.content_lookup = json_loader.get_json("content_lookup.json")
        #TODO: break this out into smaller functions so selection of
        #       builds can be more granular, i.e. create a
        #       get_build_by_name()

    def process_request(self, request):
        print('in processrequest')
        if '/' in request:
            sliced = request.split('/')
            hero = sliced[0]
            affix = sliced[1]
            try:
                level = int(affix)
                return self.get_talents_for_level(hero, level)
            except:
                return 'Lookup by hero/talent not implemented'
        else:
            return self.get_talent(request)
        return 'Not a valid request: ' + request

    def get_builds_for_hero(self, hero):
        '''Uses content_lookup and hotsapi to return formatted builds for a hero'''
        if(hero not in self.content_lookup):
            return 'Cannot find hero named {hero}'.format(hero=hero)
        #Get an array of dicts with hero talents
        hero_talents = fetch.get_hero_talents(hero)
        final_build = 'Builds for {hero}:\n'.format(hero=hero)
        builds = self.content_lookup[hero]["builds"]
        #Iterate through the builds to get talent names at each level
        for build_name, talent_choices in builds.items():
            final_build += '__{build_name}__\n'.format(build_name=build_name)
            for i, choice in enumerate(talent_choices):
                level = self.VALID_LEVELS[i]
                sort = choice
                talent_title = (talent['title'] for talent in hero_talents if talent['level']==level and talent['sort']==choice).__next__()
                final_build += '\t{level} : {talent_title}\n'.format(level=level, talent_title=talent_title)
        return final_build
    
    #def get_builds_for_hero(self, hero):
    #    if(hero not in self.heroes_json):
    #        return 'Cannot find hero {}'.format(hero)
    #    final_build = 'Builds for {}:\n'.format(hero)
    #    builds = self.heroes_json[hero]["builds"].keys()
    #    talents = self.heroes_json[hero]["talents"]
    #    for build in builds:
    #        final_build += '__{}__:\n'.format(build)
    #        choices = self.heroes_json[hero]["builds"][build]
    #        for i, choice in enumerate(choices):
    #            tier = i+1
    #            for talent in talents:
    #                if(talent["tier"] == tier and talent["choice"] == choice):
    #                    final_build += '\t{}\n'.format(talent["name"])
    #    return final_build

    def get_talents_for_hero(self, hero):
        if(hero not in self.heroes_json):
            return 'Cannot find hero {}'.format(hero)
        final_talents = 'Talents for {}:\n'.format(hero)
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
        true_name = fetch.get_hero_name(hero)
        if true_name == 'Not a valid hero':
            return true_name
        talent_list = ''
        tier = self.VALID_LEVELS.index(level) + 1        
        for t in self.heroes_json[true_name]['talents']:
            if tier == t['tier']:
                talent_list += '__{}__: {}\n\n'.format(t['name'],t['description'])
        return talent_list

    #TODO: get talents by name, maybe use string comparison with 85%
    #       threshhold of name to return relevant talents (see reddit bot)