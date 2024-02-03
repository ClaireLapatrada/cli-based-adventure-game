""" game_data2.py """
from typing import Optional, TextIO, Dict, List
import random


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - # self.x: player's location (row) in relation to map.txt
        - # self.y: player's location (column) in relation to map.txt

    Representation Invariants:
        - # self.x <= 2
        - # self.y <= 3
        - # self.inventory == [] or all([type(item) == Item for item in self.inventory])
    """

    def __init__(self, x: int, y: int) -> None:
        """ Initializes a new Player at position (x, y)."""

        self.x = x
        self.y = y
        self.inventory = []
        self.tbucks = 0
        self.victory = False

    def move(self, direction: str, world_map: list[list[int]]) -> (str, int, int):
        """ Change player's location based on the input cardinal direction.
        Return "valid" and new location if the move is valid, and return "invalid" and current location otherwise. """
        new_x, new_y = self.x, self.y

        if direction == 'north':
            new_x -= 1
        elif direction == 'south':
            new_x += 1
        elif direction == 'east':
            new_y += 1
        elif direction == 'west':
            new_y -= 1

        if 0 <= new_x < len(world_map) and 0 <= new_y < len(world_map[0]):
            return ("valid", new_x, new_y)
        else:
            return ("invalid", self.x, self.y)

    def set_location(self, x: int, y: int):
        """ set location of the player to the input location (x,y) in relation to the map in map.txt."""
        self.x = x
        self.y = y

    def acquire(self, item):
        """Acquire the item, or add the item to player's inventory"""
        print(f" -- {item.name} has been acquired! Type 'inventory' to see. -- ")
        self.inventory.append(item)

    def show_inventory(self):
        """Show player's entire inventory."""
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item.name}")

    def use_item(self, item):
        """Use the item and remove it from the player's inventory"""
        print(f" -- {item.name} has been used. --")
        self.inventory.remove(item)

    def remove_item(self, item):
        """ print the item that is dropped and remove it from player's inventory"""
        print(f"{item.name} has been dropped")
        self.inventory.remove(item)

    def check_use_item(self, item: str, location_index: int, action: Optional = None, *args):
        """Check if item can be used and use it if it is valid."""

        items = [it for it in self.inventory if it.name.strip().lower() == item.strip().lower()]
        if len(items) == 0:
            print("You don't have that item.")
            return False
        else:
            item = items[0]
            if item.in_location(self, location_index):
                if item.in_inventory(self):
                    self.use_item(item)
                    if action:
                        action(*args)
                        return True
                else:
                    print("You don't have that item yet. Come back again when you have it.")
                    return False
            else:
                if item.in_inventory(self):
                    print("This item cannot be used here.")
                    return False
                else:
                    print("You don't have that item.")
                    return False


class Item:
    """ Item class that contains information about the item's name and its usable location."""
    def __init__(self, name: str, worth: int, usable_location: int = None) -> None:
        """Initialize a new item."""
        self.name = name
        self.worth = worth
        self.usable_location = usable_location

    def in_inventory(self, player: Player):
        """check if the input item is in player's inventory"""
        return self.name in [i.name for i in player.inventory]

    def in_location(self, player: Player, loc_index: int):
        """check if item is called to use in the correct location."""
        return loc_index == self.usable_location


squirrel_interactions = {
        'chase': lambda: print("You are following a squirrel."),
        'examine': lambda: print("It's a quick and nimble squirrel.")
        }
vending_machine_interactions = {
        'press': lambda: print("You press a button on the vending machine. It dispenses an item."),
        'hit': lambda: print("You hit the vending machine. A gold coin falls out."),
        'examine': lambda: print("It's a vending machine filled with various items.")
    }
horseshoe_interactions = {
        'examine': lambda: print("It's a horseshoe that seems to bring luck."),
        'take': lambda: print("You take the horseshoe and put it in your inventory."),
        'use': lambda: print("You use the horseshoe somehow.")
    }
horse_statue_interactions = {
        'mount': lambda: print("You mount the horse statue."),
        'dismount': lambda: print("You dismount from the horse statue."),
        'nail shoe': lambda: print("You nail the horseshoe to the horse statue."),
        'open mouth': lambda: print("You open the horse statue's mouth. A letter falls out."),
    }



class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        -
        - descriptions:
        - return:

    Representation Invariants:
        -
    """
    #def __init__(self, description: str, items: List[str], exits: Dict[str, int]) -> None:
    def __init__(self, brief_description: str, long_description: str, points: int, visited: bool, unlocked: bool,
                 valid_commands: list[str]) -> None:
        self.description = brief_description
        self.long_description = long_description
        self.points = points
        self.items = []
        self.visited = visited
        self.unlocked = unlocked
        self.valid_commands = valid_commands

    def look(self):
        """ print out the description of the location being looked at."""
        return self.description

    def add_item(self, item: Item):
        """Add an item to this location."""
        self.items.append(item)

    def available_objects(self):
        """Print out all items in this location."""
        for item in self.items:
            print(item.name)

    def unlock(self):
        """Change the status of the location unlock."""
        self.unlocked = True


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - self.map: a nested list representation of this world's map
        - self.locations: a dictionary of location, in the order of how it should be visited.

    Representation Invariants:
        - self.map != []
        - TODO
    """

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.locations = self.load_location(location_data)
        self.load_items(items_data)
        self.new_game = True

    # Required method
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        self.map = []
        for line in map_data:
            row = [int(location) for location in line.strip().split()]
            self.map.append(row)
        return self.map

    def load_location(self, location_data: TextIO) -> dict[int, Location]:
        """Load location data from the given file and store it in a dictionary."""
        locations_list = {}
        lines = location_data.readlines()
        i = 0

        while i < len(lines):
            if lines[i].startswith("LOCATION"):
                location_number = int(lines[i].split()[1].strip())
                points = int(lines[i + 1].strip())
                valid_commands = lines[i + 2].strip().split(',')
                brief_description = lines[i + 3].strip()
                long_description = ""

                i += 4  # Skip to the start of long description
                while i < len(lines) and lines[i].strip() != "END":
                    long_description += lines[i].strip() + "\n"
                    i += 1

                visited = False
                unlocked = False
                location = Location(brief_description, long_description, points, visited, unlocked, valid_commands)
                locations_list[location_number] = location

            i += 1

        return locations_list

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_items(self, items_data: TextIO):
        """Load items from the given file and add them to their respective locations."""
        for line in items_data:
            parts = line.strip().split()
            location_index = int(parts[0])
            usable_index = int(parts[1])
            item_value = int(parts[2])
            item_name = ' '.join(parts[3:])

            # Create the item (assuming you have a method to create items based on the name)
            item = Item(item_name, item_value, usable_index)

            # Add the item to the respective location
            if location_index in self.locations:
                self.locations[location_index].add_item(item)

    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map."""
        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]):
            location_index = self.map[x][y]
            if location_index != -1:
                return self.locations[location_index]
        return None


# Librarian Class to Inherit from Player
class Librarian(Player):
    def __init__(self, x: int, y: int, name: str, trade_items: list):
        super().__init__(x, y)
        self.name = name
        self.trade_items = trade_items
        # self.spawn_locations = random.sample(range(2, 7), 3)  # Randomly selects 3 rooms to spawn
        self.spawn_locations = [4, 2, 3]
        self.spawned_locations = []  # Tracks locations where the NPC has already spawned
        self.interacted = False

    def check_spawn(self, player_location: tuple):
        """ Check and handle spawning of the NPC at the player's current location. """
        # print(f"Checking Librarian spawn at {player_location}. Spawn locations are {self.spawn_locations}")
        if player_location in self.spawn_locations and player_location not in self.spawned_locations:
            self.x, self.y = player_location  # Set NPC location to player location
            self.spawned_locations.append(player_location)
            print(f"A Librarian has spawned at location {player_location}... ")
            return True
        return False

    def trade_for_bucks(self, player, item):
        """ exchange player's input item for T-bucks according to its worth."""
        items = [it for it in player.inventory if it.name.strip().lower() == item.strip().lower()]
        if len(items) == 0:
            print("You don't have that item.")
        else:
            item = items[0]
            player.tbucks += item.worth
            player.remove_item(item)
            print(f"{item.name} has been traded | Tbucks balance increased by {item.worth}")

    def pity(self):
        self.interacted = True
