import time
from game_data2 import World, Item, Location, Player

def handle_command(command, player, world):
    if command.startswith('move'):
        _, direction = command.split()
        move_status, new_x, new_y = player.move(direction, world.map)

        if move_status == "valid":
            location_index = world.map[new_x][new_y]
            new_location = world.locations[location_index]
            if new_location.unlocked:
                player.x, player.y = new_x, new_y
                print(new_location.long_description)
            else:
                print("This location is locked. You can't enter yet.")
        else:
            print("You can't go that way or it's out of bounds.")

    elif command == 'quit':
        return False  # Signal to exit the game loop
    elif command == 'help':
        print("Available commands: move [direction], quit, help, look, press")
    else:
        return True  # Signal that command was not one of the basic commands
    return True  # Continue the game loop


if __name__ == "__main__":
    world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    player = Player(0, 0)

    s_short = 0.25
    print("Welcome to the Text Adventure Game!")
    print("Rules and Regulations")
    time.sleep(s_short)

    print("You wake up in your room and see a squirrel outside your window...")
    print(world.get_location(player.x, player.y).description)
    world.locations[1].unlock()  # Unlock room 1 for testing
    world.locations[2].unlock()
    continue_game = True
    while continue_game:
        current_location = world.get_location(player.x, player.y)
        # if current_location:
        #     print(current_location.long_description)
        # else:
        #     print("You are in an unknown location.")

        command = input(">> ").strip().lower()
        continue_game = handle_command(command, player, world)

        if command == 'look':
            if current_location:
                print(current_location.look())
            else:
                print("There's nothing to look at here.")
        elif command == 'item':
            print(world.get_location(player.x, player.y).items)

