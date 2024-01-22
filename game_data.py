"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO, Dict, List


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
    def __init__(self, brief_description: str, long_description: str, points: int) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.
        self.description = brief_description
        self.long_description = long_description
        self.points = points

        # self.items = items
        # self.exits = exits
        # self.visited = False

    # def look(self):
    #     return self.description if not self.visited else "You are back in the room."
    # def available_actions(self):
    #     """
    #     Return the available actions in this location.
    #     The actions should depend on the items available in the location
    #     and the x,y position of this location on the world map.
    #     """
    #
    #     # NOTE: This is just a suggested method
    #     # i.e. You may remove/modify/rename this as you like, and complete the
    #     # function header (e.g. add in parameters, complete the type contract) as needed
    #     actions = ["look", "pick up [item]", "go [direction]"]
    #     return actions

class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - # TODO

    Representation Invariants:
        - # TODO
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False

    # def move(self, direction: str, world: World):
    #     if direction in world.map[self.x][self.y].exits:
    #         new_x, new_y = world.map[self.x][self.y].exits[direction]
    #         self.x, self.y = new_x, new_y
    #     else:
    #         print("You can't go that way.")

class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of the item
        - description: description and usage of the items
        - interactions: sets of commands that can be used with the item

    Representation Invariants:
        - self.name != ""
        - self.description != ""
    """

    def __init__(self, name: str, interactions: dict = None) -> None:
        """Initialize a new item."""
        self.name = name
        if interactions is None:
            interactions = {}
        self.interactions = interactions

    def interact(self, action: str):
        """Perform an action with this item."""
        if action in self.interactions:
            self.interactions[action]()
        else:
            print(f"The action '{action}' is not available for {self.name}.")

    def show_inventory(self, player: Player):
        """Show player's entire inventory."""
        print("Inventory:")
        for item in player.inventory:
            print(f"- {item.name}: {item.description}")
    def next_painting(self, current: int = 0):
        """Move to the next paintings"""
        paintings = ["Painting 1 Clue", "Painting 2 Clue", "Painting 3 Clue", "Painting 4 Clue", "Painting 5 Clue"]
        print(paintings[current + 1])

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
art_gallery_interactions = {
    'next': lambda: next_painting()
}


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - player:
        - locations:
        - item:

    Representation Invariants:
        - # TODO
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
        # self.i

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
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
                brief_description = lines[i + 2].strip()
                long_description = ""

                i += 3  # Skip to the start of long description
                while i < len(lines) and lines[i].strip() != "END":
                    long_description += lines[i].strip() + "\n"
                    i += 1

                location = Location(brief_description, long_description, points)
                locations_list[location_number] = (location)

            i += 1

        return locations_list


    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_items(self, location_data: TextIO) -> dict[int, Location]:
        """load items"""
        pass

    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map."""
        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]):
            location_index = self.map[x][y]
            if location_index != -1:
                return self.locations[location_index]
        return None
