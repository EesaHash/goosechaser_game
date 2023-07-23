from creature import Creature
from item import Item
from location import Location

def process_locations(source):
    #Reading paths in the source and transferring them to a list(Lists of paths inside a list)
    my_file = open(source,'r')
    paths = []
    for line in my_file:
        if line != '\n':
            my_line = line.strip('\n')
            temp_list = my_line.split(" > ")
            paths.append(temp_list)

    #Creates location objects 
    location,direction,destination = 0,1,2
    location_dictionary = {}
    for path in paths:
        if path[location].rstrip() not in location_dictionary:
            location_dictionary[path[location].rstrip()] = Location(path[location].rstrip())
            location_dictionary[path[location]].set_path(path[direction].rstrip(),path[destination].rstrip())
        if path[destination].rstrip() not in location_dictionary:
            location_dictionary[path[destination].rstrip()] = Location(path[destination].rstrip())
        if path[location].rstrip() in location_dictionary:
            location_dictionary[path[location].rstrip()].set_path(path[direction].rstrip(),path[destination].rstrip())
    return list(location_dictionary.values())


def process_items(source, locations):
    #Items --- |short_name|item_name|full_desc|terror_rating|location_of_item  ---->  0,1,2,3,4 respectively
    items = []
    my_file = open(source)
    for line in my_file:
        if line != '\n':
            my_line = line.strip('\n')
            temp_list = my_line.split(" | ")
            item = Item(temp_list[0],temp_list[1],temp_list[2],int(temp_list[3]),temp_list[4])
            items.append(item)

    for location in locations:
        for item in items:
            if item.get_location() == location.get_name():
                location.add_item(item)
    return items,locations


def process_creatures(source, locations):
    #Creatures --- |name|description|terror_rating|location|direction  ---->  0,1,2,3,4 respectively
    creatures = []
    my_file = open(source)
    for line in my_file:
        if line != '\n':
            my_line = line.strip('\n')
            temp_list = my_line.split(" | ")
            creature = Creature(temp_list[0],temp_list[1],int(temp_list[2]),temp_list[3],temp_list[4])
            creatures.append(creature)

    for location in locations:
        for creature in creatures:
            if creature.get_location() == location.get_name():
                location.add_creature(creature)
    return creatures,locations


def process_exits(source, locations):
    #Exits |Exit_location|
    Exits = []
    my_file = open(source)
    for line in my_file:
        if line != '\n':
            Exit = line.strip('\n')
            Exits.append(Exit)

    for location in locations:
        for Exit in Exits:
            if Exit == location.get_name():
                location.escapable = True
    return Exits,locations
