import json
import json_loader

class BuildBuilder(object):
    def __init__(self):
        self.heroes_json = json_loader.get_json("heroes.json")
    #TODO: break this out into smaller functions so selection of
    #       builds can be more granular, i.e. create a
    #       get_build_by_name()
    def get_builds_for_hero(self, hero):
        if(hero not in self.heroes_json):
            return 'Cannot find hero {}'.format(hero)
        final_build = 'Builds for {}:\n'.format(hero)
        builds = self.heroes_json[hero]["builds"].keys()
        talents = self.heroes_json[hero]["talents"]
        for build in builds:
            final_build += '__{}__:\n'.format(build)
            choices = self.heroes_json[hero]["builds"][build]
            for i, choice in enumerate(choices):
                tier = i+1
                for talent in talents:
                    if(talent["tier"] == tier and talent["choice"] == choice):
                        final_build += '\t{}\n'.format(talent["name"])
        return final_build

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
        return found_talent

    #TODO: get talents by name, maybe use string comparison with 85%
    #       threshhold of name to return relevant talents (see reddit bot)