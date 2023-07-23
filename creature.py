class Creature:
    def __init__(self,name,description,terror_rating,location,direction='none'):

        #Creature attributes
        self.name = name
        self.description = description
        self.terror_rating = terror_rating
        self.items = []
        self.location = location
        self.direction = direction.lower()
        #Used to keep track of the tries the creature takes to catch the player(if terror_rating of the creature < player's rating)
        self.attempt = 0
    
    #Getter method to fetch the name of the creature
    def get_name(self):
        return self.name
    
    #Allows the creature to pick up an item. Also updates the terror rating
    def take(self, item):
        self.items.append(item)
        self.terror_rating += item.terror_rating
    #Used for dropping items
    def drop(self, item):
        for some_item in self.items:
            if some_item.get_name() == item.get_name():
                self.items.remove(some_item)
                self.terror_rating -= some_item.terror_rating
    
    #Returns a list of the items present at the location (obsolete method/not in use)
    def get_items(self):
        return self.items
    
    #Returns the creature's terror rating
    def get_rating(self):
        return self.terror_rating
    
    #Returns the creature's original location
    def get_location(self):
        return self.location
    
    #Returns the description
    def get_description(self):
        return self.description
    
    #Used for the look command
    def look_creature(self,player_rating):
        if player_rating - self.terror_rating >= 5:
            print('{} looks a little on-edge around you.'.format(self.name))
        elif self.terror_rating - player_rating >= 5:
            print("{} doesn't seem very afraid of you.".format(self.name))
        else:
            print("Hmm. {} is a bit hard to read.".format(self.name))

    #for player/goose only
    def show_inventory(self):
        if len(self.items) == 0:
            print('You are carrying nothing.')
        elif len(self.items) == 1:
            print('You, a {}, are carrying the following item:'.format(self.name))
            for item in self.items:
                print(' - {}'.format(item.get_long()))
        else:
            print('You, a {}, are carrying the following items:'.format(self.name))
            for item in self.items:
                print(' - {}'.format(item.get_long()))
