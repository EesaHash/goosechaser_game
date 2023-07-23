class Item:
    def __init__(self,short_name,item_name,full_desc,terror_rating,location):

        #Item attributes
        self.short_name = short_name
        self.item_name = item_name
        self.full_desc = full_desc
        self.terror_rating = terror_rating
        self.location = location
    
    #Getter method to return the items name
    def get_name(self):
        return self.short_name
    
    #Returns the long name
    def get_long(self):
        return self.item_name
    
    #Returns the description
    def get_description(self):
        return self.full_desc
 
    #Returns the terror rating
    def get_rating(self):
        return self.terror_rating
 
    #Returns the location(original)
    def get_location(self):
        return self.location
 
    #Invoked when the player uses the look command for an item
    def look_item(self):
        print('{} - Terror Rating: {}'.format(self.item_name,self.terror_rating))
