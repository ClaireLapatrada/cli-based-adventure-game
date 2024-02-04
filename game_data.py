""" game_data.py contains all the implementation of classes used in adventure.py. """
from typing import Optional, TextIO
import random


class Item:
    """
        Item class that contains information about the item's name, trading worth, and its usable location.

        Instance Attributes:
            - self.name: name of item
            - self.worth: how much an item if worth upon trade | -1 means item cannot be traded
            - self.usable_location: location where item can be used
        Representation Invariants:
            - len(self.name) >= 0
            - self.worth >= 0 or self.worth == -1
    """
    name: str
    worth: int
    usable_location: int

    def __init__(self, name: str, worth: int, usable_location: int = None) -> None:
        """Initialize a new item."""
        self.name = name
        self.worth = worth
        self.usable_location = usable_location

    def in_location(self, loc_index: int) -> bool:
        """check if item is called to use in the correct location."""
        return loc_index == self.usable_location


class Player:
    """
    A Player in the text adventure game.

    Instance Attributes:
        - self.x: player's location (row) in relation to map.txt
        - self.y: player's location (column) in relation to map.txt
        - self.inventory: items that player currently holds
        - self.tbucks: the amount of tbucks player currently has earned
        - self.step_counts = the amont of steps player has taken thoughout the game

    Representation Invariants:
        - self.x >= 0 and self.x <= 4
        - self.u >= 0 and self.y <= 5
        - self.inventory == [] or all([type(item) == Item for item in self.inventory])
        - self.tbucks >= 0
    """
    x: int
    y: int
    inventory: list
    tbucks: int
    step_counts: int
    victory: bool

    def __init__(self, x: int, y: int) -> None:
        """ Initializes a new Player at position (x, y)."""
        self.x = x
        self.y = y
        self.inventory = []
        self.tbucks = 0
        self.step_counts = 0
        self.victory = False

    def move(self, direction: str, world_map: list[list[int]]) -> (str, int, int):
        """ Change player's location based on the input cardinal direction.
        Return "valid" and new location if the move is valid,
        and return "invalid" and current location otherwise. """
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

    def set_location(self, x: int, y: int) -> None:
        """ set location of the player to the input location (x,y) in relation to the map in map.txt."""
        self.x = x
        self.y = y

    def acquire(self, item: Item) -> None:
        """Acquire the item, or add the item to player's inventory"""
        print(f" -- {item.name} has been acquired! Type 'inventory' to see. -- ")
        self.inventory.append(item)

    def show_inventory(self) -> None:
        """Show player's entire inventory."""
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item.name}")

    def use_item(self, item: Item) -> None:
        """Use the item and remove it from the player's inventory"""
        print(f" -- {item.name} has been used. --")
        self.inventory.remove(item)

    def remove_item(self, item: Item) -> None:
        """remove item from player's inventory"""
        self.inventory.remove(item)

    def in_inventory(self, item: Item) -> bool:
        """check if the input item is in player's inventory"""
        return item.name in [i.name for i in self.inventory]

    def check_use_item(self, item: str, location_index: int, action: Optional = None, *args) -> bool:
        """Check if item can be used and use it if it is valid."""

        items = [it for it in self.inventory if it.name.strip().lower() == item.strip().lower()]
        if len(items) == 0:
            print("You don't have that item.")
            return False
        else:
            item = items[0]
            if item.in_location(location_index) and self.in_inventory(item):
                self.use_item(item)
                if action:
                    action(*args)
                return True
            elif item.in_location(location_index) and not self.in_inventory(item):
                print("You don't have that item yet. Come back again when you have it.")
                return False
            elif not item.in_location(location_index) and self.in_inventory(item):
                print("This item cannot be used here.")
                return False
            else:
                print("You don't have that item.")
                return False


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - self.description: brief description of the location
        - self.long_description: long description of the location
        - self.points: points that could be earned in a location
        - self.items: items loaded within the location
        - self.visited: whether the player has visited the location
        - self.unlocked: whether the location has been unlocked for the player to access
        - self.valid_commands = the commands that can be used in this specifc locatio
        - self.hint: hints for the puzzle within this specific location

    Representation Invariants:
        - len(self.description) >= 0
        - len(self.long_description) >= 0
        - self.points >= 0
    """
    description: str
    long_description: str
    points: int
    items: list
    unlocked: bool
    valid_commands: list[str]
    hint: str

    def __init__(self, brief_description: str, long_description: str, unlocked: bool,
                 valid_commands: list[str]) -> None:
        self.description = brief_description
        self.long_description = long_description
        self.items = []
        self.unlocked = unlocked
        self.valid_commands = valid_commands
        self.hint = self.long_description.split('\n')[-2]

    def look(self) -> str:
        """ print out the description of the location being looked at."""
        return self.description

    def add_item(self, item: Item) -> None:
        """Add an item to this location."""
        self.items.append(item)

    def available_objects(self) -> None:
        """Print out all items in this location."""
        for item in self.items:
            print(item.name)

    def unlock(self) -> None:
        """Change the status of the location unlock."""
        self.unlocked = True


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - self.map: a nested list representation of this world's map
        - self.locations: a list of location, in the order of how it should be visited.


    Representation Invariants:
        - self.map != []
        - self.locations != []
    """
    map: list[list[int]]
    locations: dict[int, Location]
    load_items: dict[int, Item]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        self.map = self.load_map(map_data)
        self.locations = self.load_location(location_data)
        self.load_items(items_data)

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
                ok_commands = lines[i + 2].strip().split(',')
                brief_description = lines[i + 3].strip()
                long_description = ""

                i += 4  # Skip to the start of long description
                while i < len(lines) and lines[i].strip() != "END":
                    long_description += lines[i].strip() + "\n"
                    i += 1
                unlocked = False
                location = Location(brief_description, long_description, unlocked, ok_commands)
                locations_list[location_number] = location

            i += 1

        return locations_list

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_items(self, items_data: TextIO) -> None:
        """Load items from the given file and add them to their respective locations."""
        for line in items_data:
            parts = line.strip().split()
            location_index = int(parts[0])
            usable_index = int(parts[1])
            item_value = int(parts[2])
            item_name = ' '.join(parts[3:])

            item = Item(item_name, item_value, usable_index)

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
    """A Libraian - NPC like class that extends from Player.

    Instance Attributes:
        - self.name: name of the Librarian
        - self.trade_items: the items that can be traded for from the Librarian
        - self.spawn_locations: a list of location_index that librarian can spawn in
        - self.spawned_locations: a list of location_index that librarian has already spawned in
        - self.interacted: boolean value of whether librarian in the specific location has been interacted with

    Representation Invariants:
        - self.map != []
        - self.locations != []
        - len(self.spawn_locations) >= 0
    """
    x: int
    y: int
    name: str
    trade_items: list
    spawn_locations: list[int]
    spawned_locations: list[tuple]
    interacted: bool

    def __init__(self, x: int, y: int, name: str) -> None:
        super().__init__(x, y)
        self.name = name
        # Randomly selects 3 rooms to spawn
        # self.spawn_locations = random.sample(range(2, 6), 3)
        self.spawn_locations = [2, 3, 4]
        self.spawned_locations = []
        self.interacted = False

    def bargain(self, player: Player) -> None:
        """ Randomly add tbucks to the player upon command [bargain] is called."""
        added = random.choice([20, 25, 50, 75, 100, 150])
        player.tbucks += added
        print(f"Tbucks incresed by {added}")
        print(f"Tbucks balance: {player.tbucks}")

    def check_spawn(self, player_location: tuple) -> bool:
        """ Check and handle spawning of the NPC at the player's current location. """
        # Check if the librarian is supposed to spawn at the player's current location and hasn't already spawned there
        if player_location in self.spawn_locations and player_location not in self.spawned_locations:
            self.x, self.y = player_location  # Set NPC location to player location
            self.spawned_locations.append(player_location)
            self.interacted = False  # Reset interacted to allow a new interaction
            print(f"A Librarian has spawned at location {player_location}... ")
            return True
        return False

    def trade_for_bucks(self, player: Player, item: str) -> None:
        """ exchange player's input item for T-bucks according to its worth."""
        items = [it for it in player.inventory if it.name.strip().lower() == item.strip().lower()]

        if len(items) == 0:
            print("You don't have that item.")
        else:
            item = items[0]
            if item.worth == -1:
                print("Why are you trading something you need? ")
            else:
                player.tbucks += item.worth
                player.remove_item(item)
                print(f"{item.name} has been traded | Tbucks balance increased by {item.worth}")
                print(f"Tbucks balance: {player.tbucks}")
