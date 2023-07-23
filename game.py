import sys
from creature import Creature
from item import Item
from location import Location
from preprocessing import process_locations,process_exits,process_items,process_creatures

#Used for goosechasers' navigation and commands are for user_input validation
compass = ['north','northeast','east','southeast','south','southwest','west','northwest']
valid_commands = ['north','n','northeast','ne','east','e','southeast','se','south','s','southwest','sw','west','w','northwest','nw','look','inv','flee','honk','y','wait','quit','look','l','help']

#Checks for if the number of arguments provided are insufficient
number_of_arguments = len(sys.argv)
if number_of_arguments < 5:
	print('Usage: python3 game.py <PATHS> <ITEMS> <CHASERS> <EXITS>')
	quit()

#Initializes objects from files and handles a Filenotfound exception if a file doesnt exist
try:
	locations = process_locations(sys.argv[1])
	items,locations = process_items(sys.argv[2],locations)
	creatures,locations = process_creatures(sys.argv[3],locations)
	exits,locations = process_exits(sys.argv[4],locations)
#Quits if an empty paths file is provided
	if len(locations) == 0:
		print('The game cannot run without any rooms :(')
		quit()
#Quits if an empty chasers file is provided
	if len(creatures) == 0:
		print('There is nothing chasing you!')
		quit()
except FileNotFoundError:
	print('You have specified an invalid configuration file.')
	quit()


#Creation of a dictionary to handle locations....easier to just find locations by calling their name
Locations = {}
for location in locations:
	Locations[location.get_name()] = location


#Initializing first location and player(Goose), Starting location is the first location in the paths file i.e. first element of the dictionary
starting_location = 0
current_location = list(Locations.values())[starting_location].get_name()
goose = Creature('goose','You are a goose, You are probably quite terrifying.',5,current_location)

#Threat detection function i.e placing '[C]' if goosechaser in nearby location
def detect_threat():
	for location,loc_object in Locations.items():
		if current_location == location:
			if loc_object.move('south') in Locations:
				ls = Locations[loc_object.move('south')].creatures
				if len(ls) > 0:
					loc_object.south = " [C] "
				else:
					loc_object.south = " [ ] "
			if loc_object.move('north') in Locations:
				ls = Locations[loc_object.move('north')].creatures
				if len(ls) > 0:
					loc_object.north = " [C] "
				else:
					loc_object.north = " [ ] "
			if loc_object.move('east') in Locations:
				ls = Locations[loc_object.move('east')].creatures
				if len(ls) > 0:
					Locations[current_location].east = "-[C]"
				else:
					loc_object.east = "-[ ]"
			if loc_object.move('west') in Locations:
				ls = Locations[loc_object.move('west')].creatures
				if len(ls) > 0:
					loc_object.west = "[C]-"
				else:
					loc_object.west = "[ ]-"
			if loc_object.move('northeast') in Locations:
				ls = Locations[loc_object.move('northeast')].creatures
				if len(ls) > 0:
					loc_object.northeast = "[C]"
				else:
					loc_object.northeast = "[ ]"
			if loc_object.move('northwest') in Locations:
				ls = Locations[loc_object.move('northwest')].creatures
				if len(ls) > 0:
					loc_object.northwest = "[C]"
				else:
					loc_object.northwest = "[ ]"
			if loc_object.move('southeast') in Locations:
				ls = Locations[loc_object.move('southeast')].creatures
				if len(ls) > 0:
					loc_object.southeast = "[C]"
				else:
					loc_object.southeast = "[ ]"
			if loc_object.move('southwest') in Locations:
				ls = Locations[loc_object.move('southwest')].creatures
				if len(ls) > 0:
					loc_object.southwest = "[C]"
				else:
					loc_object.southwest = "[ ]"

#Allows goosechasers to take their turns
def take_turns():
	for creature in creatures:
		found = 0
		for location,loc_object in Locations.items():
			if found == 1:
				break
			for chaser in loc_object.creatures:
				if creature.get_name() == chaser.get_name():
					found = 1

					if location == current_location:
						if goose.get_rating() < chaser.get_rating():
							print()
							print('{} is trying to catch you!'.format(chaser.get_name()))
							print("Oh no, you've been caught!")
							print('========= GAME OVER =========')
							quit()

						if goose.get_rating() > chaser.get_rating():
							if chaser.attempt == 0:
								print()
								print('{} is trying to catch you!'.format(chaser.get_name()))
								print('But your presence still terrifies them...')
								chaser.attempt += 1

							elif chaser.attempt == 1:
								print()
								print('{} is trying to catch you!'.format(chaser.get_name()))
								print("Oh no, you've been caught!")
								print('========= GAME OVER =========')
								quit()

                    #If the goosechaser is not in the same room as the player
					if location != current_location:
						chaser.attempt = 0
						successful = 0
						for direction in compass:
							#move returns a location name in a specific direction if it exists
							if loc_object.move(direction) in Locations:
								if loc_object.move(direction) == current_location:
									Locations[loc_object.move(direction)].add_creature(chaser)
									loc_object.remove_creature(chaser)
									chaser.direction = direction
									print()
									print("{} has arrived at {}.".format(chaser.get_name(),current_location))
									successful = 1
                        #If the goosechaser is unable to reach the player directly, it proceeds to
						#take an item if and if unsuccessful, move to its default direction and if thats impossible then
						#moves in a direction clockwise to its default direction
						if successful == 0:
							if len(loc_object.items) > 0:
								chaser.take(loc_object.items[0])
								loc_object.remove_item(loc_object.items[0])
								break
							else:
								if loc_object.move(chaser.direction) in Locations:
									Locations[loc_object.move(chaser.direction)].add_creature(chaser)
									loc_object.remove_creature(chaser)
									break
								else:
									i = 0
									for direction in compass:
										if direction == chaser.direction:
											break
										i += 1
									if i == 7:
										i = 0
									while i < len(compass):
										if loc_object.move(compass[i]) in Locations:
											chaser.direction = compass[i]
											Locations[loc_object.move(chaser.direction)].add_creature(chaser)
											loc_object.remove_creature(chaser)
											break
										i += 1


#Displays information about the location if moved into a new locations
def show_info():
	output_string = ''
	print('You are now at: {}.'.format(current_location))
	if len(Locations[current_location].items) > 0:
		for item in Locations[current_location].items:
			output_string += ' ' + item.get_description()
	if len(Locations[current_location].creatures) > 0:
		for creature in Locations[current_location].creatures:
			output_string += ' ' + creature.get_description()
	if output_string != '':
		temp_string = output_string.lstrip()
		output_string = temp_string.rstrip()
		print(output_string)
	if len(Locations[current_location].items) == 0 and len(Locations[current_location].creatures) == 0:
		print('There is nothing here.')
	if Locations[current_location].escapable is True:
		print('The path to freedom is clear. You can FLEE this place.')

#removed_creature is used to quit the program if every chaser has been successfully scared off permenantly
removed_creatures = 0
start = True
#Beginning of the main program
while True:
    #Shows the location and the map at the beginning of the program
	if start is True:
		detect_threat()
		Locations[current_location].map()
		show_info()
		start = False


	#Asks for the players's command
	print()
	player_command = input('>> ')
	player_command = player_command.lower()

	if (player_command not in valid_commands) and ('look' not in player_command) and ('take' not in player_command) and ('drop' not in player_command):
		print("You can't do that.")

    #Look command
	if player_command == 'look' or player_command == 'l':
		detect_threat()
		Locations[current_location].map()
		show_info()


	if 'look' in player_command and ' ' in player_command:
		command,subject_to_look = player_command.split(' ')
		found = False
		#Looking at the player/goose/yourself
		if subject_to_look == 'me':
			print('You are a {}. You are probably quite terrifying.'.format(goose.get_name()))
			print('In fact, you have a terror rating of: {}'.format(goose.terror_rating))
			found = True
		#Looking Items
		for item in Locations[current_location].items:
			if subject_to_look == item.get_name():
				item.look_item()
				found = True
		for item in goose.get_items():
			if subject_to_look == item.get_name():
				item.look_item()
				found = True
		#Looking creatures
		for creature in Locations[current_location].creatures:
			if subject_to_look == creature.get_name().lower():
				creature.look_creature(goose.get_rating())
				found = True
		#Looking here
		if subject_to_look == 'here':
			if len(Locations[current_location].items) == 0:
				print('There is nothing here.')
			for item in Locations[current_location].items:
				print('{:16}| {}'.format(item.get_name().upper(),item.get_long()))
			found = True
		#If the subject is not found in any of the conditions above
		if found is False:
			print("You don't see anything like that here.")
    
	#Implementation of the take command
	if 'take' in player_command and ' ' in player_command:
		command,item_to_take = player_command.split(' ')
		taken = False
		for item in Locations[current_location].items:
			if item.get_name().lower() == item_to_take:
				goose.take(item)
				Locations[current_location].remove_item(item)
				print('You pick up the {}.'.format(item.get_long()))
				taken = True
		if taken is False:
			print("You don't see anything like that here.")
		if taken is True:
			take_turns()

    #Implementation of the drop command
	if 'drop' in player_command and ' ' in player_command:
		command,item_to_drop = player_command.split(' ')
		dropped = False
		for item in goose.items:
			if item.get_name().lower() == item_to_drop:
				goose.drop(item)
				Locations[current_location].add_item(item)
				print('You drop the {}.'.format(item.get_long()))
				dropped = True
		if dropped is False:
			print("You don't have that in your inventory.")
		if dropped is True:
			take_turns()
    
	#Shows what the goose/player is carrying
	if player_command == 'inv':
		goose.show_inventory()
    
	#Used to flee a location if an exit exists
	if player_command == 'flee':
		if Locations[current_location].escapable is True:
			print('You slip past the dastardly Goosechasers and run off into the wilderness! Freedom at last!')
			print('========= F R E E D O M =========')
			quit()
		else:
			print("There's nowhere you can run or hide! Find somewhere else to FLEE.")
    
	#Wait command, allows other creatures to take their turns sequentially creature1 --> creature2 --> creature3 etc....
	if player_command == 'wait':
		print('You lie in wait.')
		take_turns()
    
	#Honk and y commands used to scare away goosechasers permenantly(if possible)
	if player_command == 'honk' or player_command == 'y':
		if len(Locations[current_location].creatures) == 0:
			print('All shall quiver before the might of the goose! HONK!')
		else:
			print('You sneak up behind your quarry and honk with all the force of a really angry airhorn! HONK!')
			for i in range(0,len(Locations[current_location].creatures)):
				for creature in Locations[current_location].creatures:
					if creature.get_rating() < goose.get_rating():
						print('{} is spooked! They flee immediately!'.format(creature.get_name()))
						Locations[current_location].remove_creature(creature)
						removed_creatures += 1
					elif creature.get_rating() > goose.get_rating():
						print('{} is not spooked :('.format(creature.get_name()))
		if removed_creatures == len(creatures):
			print()
			print("None can stand against the power of the goose!")
			print('========= V I C T O R Y =========')
			quit()
		take_turns()
    
	#Directional commands for the player/goose's navigation
	if player_command == 'north' or player_command == 'n':
		moved = 0
		for location,loc_object in Locations.items(): #location is the key of the Locations dict and loc_object is the location object tied to the key.
			if current_location == location:
				if loc_object.move('north') in Locations:  #loc_object.move('direction') returns the name of a location in the direction specified
					current_location = Locations[loc_object.move('north')].get_name()
					moved = 1   #Flag used to verify if the player has moved
					break
		if moved == 1:  #If the player moves successfully, this code below executes
			print('You move north, to {}.'.format(current_location))
			take_turns()
			detect_threat()
			Locations[current_location].map()
			show_info()
		if moved == 0:  #If the goose/player is unable to move in the specified direction
			print("You can't go that way.")

#All the directional commands below are a repetition of whats above(work similarly) Tried to condense it to just a function but the code was breaking..
	if player_command == 'northwest' or player_command == 'nw':
		moved = 0
		for location,loc_object in Locations.items():
			if current_location == location:
				if loc_object.move('northwest') in Locations:
					current_location = Locations[loc_object.move('northwest')].get_name()
					moved = 1
					break
		if moved == 1:
			print('You move northwest, to {}.'.format(current_location))
			take_turns()
			detect_threat()
			Locations[current_location].map()
			show_info()

		if moved == 0:
			print("You can't go that way.")

	if player_command == 'northeast' or player_command == 'ne':
		moved = 0
		for location,loc_object in Locations.items():
			if current_location == location:
				if loc_object.move('northeast') in Locations:
					current_location = Locations[loc_object.move('northeast')].get_name()
					moved = 1
					break
		if moved == 1:
			print('You move northeast, to {}.'.format(current_location))
			take_turns()
			detect_threat()
			Locations[current_location].map()
			show_info()

		if moved == 0:
			print("You can't go that way.")

	if player_command == 'south' or player_command == 's':
		moved = 0
		for location,loc_object in Locations.items():
			if current_location == location:
				if loc_object.move('south') in Locations:
					current_location = Locations[loc_object.move('south')].get_name()
					moved = 1
					break
		if moved == 1:
			print('You move south, to {}.'.format(current_location))
			take_turns()
			detect_threat()
			Locations[current_location].map()
			show_info()
		if moved == 0:
			print("You can't go that way.")

	if player_command == 'southeast' or player_command == 'se':
		moved = 0
		for location,loc_object in Locations.items():
			if current_location == location:
				if loc_object.move('southeast') in Locations:
					current_location = Locations[loc_object.move('southeast')].get_name()
					moved = 1
					break
		if moved == 1:
			print('You move southeast, to {}.'.format(current_location))
			take_turns()
			detect_threat()
			Locations[current_location].map()
			show_info()

		if moved == 0:
			print("You can't go that way.")

	if player_command == 'southwest' or player_command == 'sw':
		moved = 0
		for location,loc_object in Locations.items():
			if current_location == location:
				if loc_object.move('southwest') in Locations:
					current_location = Locations[loc_object.move('southwest')].get_name()
					moved = 1
					break
		if moved == 1:
			print('You move southwest, to {}.'.format(current_location))
			take_turns()
			detect_threat()
			Locations[current_location].map()
			show_info()

		if moved == 0:
			print("You can't go that way.")

	if player_command == 'east' or player_command == 'e':
		moved = 0
		for location,loc_object in Locations.items():
			if current_location == location:
				if loc_object.move('east') in Locations:
					current_location = Locations[loc_object.move('east')].get_name()
					moved = 1
					break
		if moved == 1:
			print('You move east, to {}.'.format(current_location))
			take_turns()
			detect_threat()
			Locations[current_location].map()
			show_info()

		if moved == 0:
			print("You can't go that way.")


	if player_command == 'west' or player_command == 'w':
		moved = 0
		for location,loc_object in Locations.items():
			if current_location == location:
				if loc_object.move('west') in Locations:
					current_location = Locations[loc_object.move('west')].get_name()
					moved = 1
					break
		if moved == 1:
			print('You move west, to {}.'.format(current_location))
			take_turns()
			detect_threat()
			Locations[current_location].map()
			show_info()

		if moved == 0:
			print("You can't go that way.")

    #Help command
	if player_command == 'help':
		print('{:16}- Shows some available commands.'.format('HELP'))
		print('{:16}- Lists all the items in your inventory.'.format('INV'))
		print('{:16}- Takes an item from your current location.'.format('TAKE <ITEM>'))
		print('{:16}- Drops an item at your current location.'.format('DROP <ITEM>'))
		print()
		print('{:16}- Lets you see the map/location again.'.format('LOOK or L'))
		print('{:16}- Lets you see an item in more detail.'.format('LOOK <ITEM>'))
		print('{:16}- Sometimes, you just have to admire the feathers.'.format('LOOK ME'))
		print('{:16}- Sizes up a nearby creature.'.format('LOOK <CREATURE>'))
		print('{:16}- Shows a list of all items in the room.'.format('LOOK HERE'))
		print()
		print('{:16}- Moves you to the northwest.'.format('NORTHWEST or NW'))
		print('{:16}- Moves you to the north.'.format('NORTH or N'))
		print('{:16}- Moves you to the northeast.'.format('NORTHEAST or NE'))
		print('{:16}- Moves you to the east.'.format('EAST or E'))
		print()
		print('{:16}- Moves you to the southeast.'.format('SOUTHEAST or SE'))
		print('{:16}- Moves you to the south.'.format('SOUTH or S'))
		print('{:16}- Moves you to the southwest.'.format('SOUTHWEST or SW'))
		print('{:16}- Moves you to the west.'.format('WEST or W'))
		print()
		print('{:16}- Attempt to flee from your current location.'.format('FLEE '))
		print('{:16}- Attempt to scare off all creatures in the same location.'.format('HONK or Y'))
		print('{:16}- Do nothing. All other creatures will move around you.'.format('WAIT'))
		print('{:16}- Ends the game. No questions asked.'.format('QUIT'))
    
	#Quit terminates the whole program
	if player_command == 'quit':
		print('Game terminated.')
		quit()
