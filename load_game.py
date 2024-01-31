import json
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []

class Item:
    def __init__(self, name):
        self.name = name

class Location:
    def __init__(self, description, visited=False):
        self.description = description
        self.visited = visited

class World:
    def __init__(self):
        self.locations = {}

def save_game(player, world, file_name='savegame.txt'):
    save_data = {
        'player_x': player.x,
        'player_y': player.y,
        'player_inventory': [item.name for item in player.inventory],
        'visited_locations': {loc_id: loc.visited for loc_id, loc in world.locations.items()}
    }
    with open(file_name, 'w') as file:
        json.dump(save_data, file)
    print("Game saved.")


def load_game(player, world, file_name='savegame.txt'):
    with open(file_name, 'r') as file:
        save_data = json.load(file)

    player.x = save_data['player_x']
    player.y = save_data['player_y']
    player.inventory = [Item(name) for name in save_data['player_inventory']]

    for loc_id, visited in save_data['visited_locations'].items():
        world.locations[loc_id].visited = visited
    print("Game loaded.")
