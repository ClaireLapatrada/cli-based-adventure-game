from typing import Optional, TextIO, Dict, List


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

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False

    # def move(self, direction: str, exits: dict):
    #     if direction in exits:
    #         new_x, new_y = exits[direction]
    #         self.x, self.y = new_x, new_y
    #     else:
    #         print("You can't go that way.")
    def move(self, direction: str, world_map: list[list[int]]) -> (str, int, int):
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
        self.x = x
        self.y = y

class Item:
    def __init__(self, name: str, interactions: dict = None) -> None:
        """Initialize a new item." ""
        self.name = name
        if interactions is None:
            interactions = {}
        self.interactions = interactions
        pass
        """
        self.name = name
        self.interactions = interactions

    def press(self):
        """Perform an action with this item based on its type and the action provided."""
        if self.name == "Vending Machine":
            print("vending machine")
            self.acorn_vending()
        elif self.name == "Squirrel":
            print("Ouch you cannot hurt the Squirrel")
        else:
            print(f"The action '{action}' is not available for {self.name}.")

    def acorn_vending(self):
        password = input('Press')
        while password != 'abc':
            password = input('put in pin pad')
        print('successful')

    def show_inventory(self, player: Player):
        """Show player's entire inventory."""
        print("Inventory:")
        for item in player.inventory:
            print(f"- {item.name}: {item.description}")

    def next_painting(self, current: int = -1):
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
    def __init__(self, brief_description: str, long_description: str, points: int, visited: bool, unlocked: bool) -> None:
        self.description = brief_description
        self.long_description = long_description
        self.points = points
        self.items = []
        self.visited = visited
        self.unlocked = unlocked

    def look(self):
        return self.description
    def add_item(self, item: Item):
        """Add an item to this location."""
        self.items.append(item)

    def available_objects(self):
        """Print out all items in this location."""
        for item in self.items:
            print(item.name)

    def unlock(self):
        self.unlocked = True

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
        self.load_items(items_data)

    #Required method
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

                visited = False
                unlocked = False
                location = Location(brief_description, long_description, points, visited, unlocked)
                locations_list[location_number] = (location)

            i += 1

        return locations_list


    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_items(self, items_data: TextIO):
        """Load items from the given file and add them to their respective locations."""
        for line in items_data:
            parts = line.strip().split()
            location_index = int(parts[0])
            item_name = ' '.join(parts[1:])

            # Create the item (assuming you have a method to create items based on the name)

            # Add the item to the respective location
            if location_index in self.locations:
                self.locations[location_index].add_item(item_name)

    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map."""
        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]):
            location_index = self.map[x][y]
            if location_index != -1:
                return self.locations[location_index]
        return None