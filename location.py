class Location:
	def __init__(self,name):

		#Location attributes
		self.name = name
		self.items = []
		self.creatures = []
		self.escapable = False

        #Additional attributes for navigation and displaying a map
		self.northwest,self.nw_room,self.bar_northwest = '   ','empty','    '
		self.northeast,self.ne_room,self.bar_northeast = '   ','empty','    '
		self.north,self.n_room,self.bar_north = '     ','empty','   '
		self.east,self.e_room = '    ','empty'
		self.south,self.s_room,self.bar_south = '     ','empty','   '
		self.southeast,self.se_room,self.bar_southeast = '   ','empty','    '
		self.southwest,self.sw_room,self.bar_southwest = '   ','empty','    '
		self.west,self.w_room= '    ','empty'
    
	#Used to tie locations with directions in preprocessing
	def set_path(self, direction, dest):
		if direction.lower() == "north":
			self.north = " [ ] "
			self.n_room = dest
			self.bar_north = ' | '
		if direction.lower() == "south":
			self.south = " [ ] "
			self.s_room = dest
			self.bar_south = ' | '
		if direction.lower() == "northwest":
			self.northwest = "[ ]"
			self.nw_room = dest
			self.bar_northwest = '   \\'
		if direction.lower() == "northeast":
			self.northeast = "[ ]"
			self.ne_room = dest
			self.bar_northeast = '/'
		if direction.lower() == 'east':
			self.east = "-[ ]"
			self.e_room = dest
		if direction.lower() == 'southeast':
			self.southeast = "[ ]"
			self.se_room = dest
			self.bar_southeast = "\\   "
		if direction.lower() == "southwest":
			self.southwest = "[ ]"
			self.sw_room = dest
			self.bar_southwest = '   /'
		if direction.lower() == 'west':
			self.west = "[ ]-"
			self.w_room = dest
    
	#Used to add an item to the location
	def add_item(self, item):
		self.items.append(item)
    
	#Removes an item from the location
	def remove_item(self,item):
		for some_item in self.items:
			if some_item.get_name() == item.get_name():
				self.items.remove(some_item)
    
	#Adds a creature to the location
	def add_creature(self,creature):
		self.creatures.append(creature)
    
	#Removes a creature from the location
	def remove_creature(self,creature):
		for some_creature in self.creatures:
			if some_creature.get_name() == creature.get_name():
				self.creatures.remove(some_creature)
    
	#Getter method used to return the name of the location
	def get_name(self):
		return self.name
    
	#Used to show a map when the look or directional commands are invoked
	def map(self):
		print('{}{}{}'.format(self.northwest,self.north,self.northeast).rstrip())
		print('{}{}{}'.format(self.bar_northwest,self.bar_north,self.bar_northeast).rstrip())
		print('{}{}{}'.format(self.west,'[x]',self.east).rstrip())
		print('{}{}{}'.format(self.bar_southwest,self.bar_south,self.bar_southeast).rstrip())
		print('{}{}{}'.format(self.southwest,self.south,self.southeast).rstrip())
    
	#Returns the names of the locations accessible in each direction.
	def move(self, direction):
		if direction == "north":
			return self.n_room
		if direction == "south":
			return self.s_room
		if direction == "northwest":
			return self.nw_room
		if direction == "northeast":
			return self.ne_room
		if direction == "east":
			return self.e_room
		if direction == "southeast":
			return self.se_room
		if direction == "southwest":
			return self.sw_room
		if direction == "west":
			return self.w_room
