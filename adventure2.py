"""The main adventure.py file. Click run on this file to start the game. """
import time
from game_data2 import World, Item, Location, Player, Librarian
import json

def handle_location0(com, pl, w):
    print("You wake up in your room and see a squirrel outside your window...")
    print("type 'follow squirrel'")
    com = input(">> ").strip().lower()
    while not com.startswith('follow'):
        print("do you need TYPING LESSSONS")
        com = input(">> ").strip().lower()
    w.locations[1].unlock()
    player.set_location(0, 1)
    return True

# Location-1 (Vending) Helper Functions
def handle_location1(com, pl, w):
    """Start location 1's events if it has not been cleared yet, else notify the player."""
    if "vending" in com:
        if w.locations[2].unlocked:
            print("Vending Machine Puzzle has been solved. No other useful clues. ")
        else:
            return passkey_vending(pl, w)
    # else:
    #     print("Nothing interesting happens.")
    return True


def passkey_vending(pl, w):
    """Ask player for input for the vending machine, drop item when the correct code has been input.
    Handle all other commands."""
    print("The vending machine has no slot for coins, only an alphanumeric keypad.")
    while True:
        inp = input(">> ").strip().lower()
        if inp.startswith("inspect"):
            print("You inspect the vending machine closely.")
        elif inp == "type code":
            code = input("Enter code: ").strip()
            if code == "correct_code":  # Replace with the actual code
                print("You hear a click sound as the next room is unlocked.")
                w.locations[2].unlock()  # Assuming location 2 is the next one
                for item in w.get_location(pl.x, pl.y).items:
                    pl.acquire(item)
                return True
            else:
                print("Nothing happens. It seems to be the wrong code.")
        elif inp == "quit":
            return False
        else:
            print("You are not sure what to do with that.")


# Location 2 - (Hallway with Painting)
current_painting_index = 0


def handle_location2(com, pl, w):
    """Start location 2's events if it has not been cleared yet, else notify the player."""
    global current_painting_index

    if com == 'talk':
        if w.locations[3].unlocked:
            print("Talking with paintings won't solve more of your problems.")
        else:
            return paintings_hint()
    elif com == 'next':
        current_painting_index += 1
        return paintings_hint()
    # else:
    #     print("You can't do that here.")

    return True


def paintings_hint():
    """move to the next painting and call the door puzzle onve all paintings have been visited.
    Handle all other commands."""
    global current_painting_index
    paintings = [
        "get ready to receive words of wisdom from the paintings",
        "Seek and you shall find.",
        "Every little piece matters.",
        "Courage opens new paths.",
        "Resilience lies within.",
        "Eternal wisdom hides in chaos.",
        "Time will tell."
    ]
    if current_painting_index < len(paintings):
        print(paintings[current_painting_index])
    else:
        # Once all paintings have been viewed, prompt the door puzzle
        return door_puzzle()
    return True


def door_puzzle():
    """Ask user for input to the door puzzle, with animation when revealing the correct code.
    Handle all other commands."""
    solution = "secret"
    while True:
        print("\nYou stand before a door with no handles, only a panel with letters.")
        print("_ _ _ _ _ _")
        user_input = input(">> ").strip().lower()

        # Animation for revealing each letter
        display = ['_', '_', '_', '_', '_', '_']
        for i, char in enumerate(user_input):
            if i < len(display):
                display[i] = char
                print("\r" + " ".join(display), end="")
                time.sleep(0.5)

        # Check the solution after the animation
        if user_input == solution:
            print("\nThe door clicks open, revealing a new path ahead.")
            world.locations[3].unlock()
            return True
        elif user_input == "quit":
            print("\nQuitting the puzzle.")
            return False
        else:
            print("\nNothing happens. Perhaps the clues in the paintings can help.")


# Location 3 - (Horse Statue)
def handle_location3(com, pl, w):
    command_specific = ['trade']
    """Start location 3 events if it has not been cleared yet, else notify the player."""
    if com == 'look':
        if w.locations[4].unlocked:
            print("The horse isn't here anymore.")
        else:
            return horse_statue_shoe(com, pl, w)
    elif command not in command_specific:
        print("Maybe you should look around the statue. What might the horse statue be seeking from you?")
    return True


def horse_statue_shoe(com, pl, w):
    """Ask player for input to use the horse shoe, call horse_statue_read() once the correct item has been used.
    Handle all other commands."""
    print("Hmmm... the horse's front left foot doesn't look quite right. It's missing something.")
    while True:
        inp = input(">> ").strip().lower()
        if len(inp.split()) >= 2:
            do, item = inp.split(' ', 1)
            if do == 'use':
                pl.check_use_item(item, 3, horse_statue_read, com, pl, w)
        elif inp == "use":
            print("Use what?")
        elif inp == "quit":
            return False
        elif inp == "inventory":
            pl.show_inventory()
        elif inp.startswith("move"):
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")


def horse_statue_read(com, pl, w):
    """Ask player for the right command to inspect the letter and keep it, call horse_statue_go when completed.
    Handle all other commands."""
    print("The horse's mouth opened up. Seems like something is in there.")
    while True:
        inp = input(">> ").strip().lower()
        if inp == 'inspect':
            print("There is a mystery letter in here. It reads ['astronomeeee']")
            print()
            print("The letter might be useful later on. You might want to keep it.")
            inp = input(">> ").strip().lower()
            while not inp.startswith('keep'):
                print("THE LETTER MIGHT BE USEFUL LATER ON. YOU MIGHT WANT TO KEEP IT")
                inp = input(">> ").strip().lower()
            for item in w.get_location(pl.x, pl.y).items:
                pl.acquire(item)
            horse_statue_go(com, pl, w)
        elif inp == "quit":
            return False
        elif inp == "inventory":
            pl.show_inventory()
        elif inp == "move":
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")


def horse_statue_go(com, pl, w):
    """Ask user for the correct command, print progress bar for riding the horse,
    unlock and update new location as arrived. Print new location description. Handle all other commands."""
    print("Great! Now we have a letter. Oh wait.. The horse statue is moving!? To where? Let's mount on to see.")
    while True:
        inp = input(">> ").strip().lower()
        if inp == 'mount':
            w.locations[4].unlock()
            print("weeeee let's go!")
            print_progress_bar("riding the horse", duration=5, width=30)
            location_index = w.map[2][0]
            new_location = w.locations[location_index]
            pl.x, pl.y = 2, 0
            print(new_location.long_description)
        elif inp == "quit":
            return False
        elif inp == "inventory":
            pl.show_inventory()
        elif inp == "move":
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")

def handle_librarian_interaction(com, pl, librarian, w):
    #print("you're in a territory with a librarian that can trade with you")
    if com.startswith('loot'):
        # Example trade logic
        print("Trade begins: use command like\n"
              "[trade: trade unused item for Tbucks, drop: to drop items, bargain: to ask nicely for MORE Tbucks]\n"
              "[pity: leave the poor librian alon WARNING: you cannot loot this poor soul again")
    while True:
        user_input = input(">> ").strip().lower()
        if user_input == 'trade':
            print("trade logic #TODO")
        elif user_input.startswith('drop'):
            print("drop logic #TODO")
        elif user_input.startswith('bargain'):
            player.tbucks += 1
            print(player.tbucks)
        elif user_input.startswith('pity'):
            print("Libraian: Phew! Thank you for leaving me alone")
            time.sleep(0.02)
            print("Type 'look' to keep exploring the room")
            return False


    # Add more interaction types as needed
    #
    # while True:
    #     print("\nYou stand before a door with no handles, only a panel with letters.")
    #     print("_ _ _ _ _ _")
    #     user_input = input(">> ").strip().lower()
    #
    #     # Animation for revealing each letter
    #     display = ['_', '_', '_', '_', '_', '_']
    #     for i, char in enumerate(user_input):
    #         if i < len(display):
    #             display[i] = char
    #             print("\r" + " ".join(display), end="")
    #             time.sleep(0.5)
    #
    #     # Check the solution after the animation
    #     if user_input == solution:
    #         print("\nThe door clicks open, revealing a new path ahead.")
    #         world.locations[3].unlock()
    #         return True
    #     elif user_input == "quit":
    #         print("\nQuitting the puzzle.")
    #         return False
    #     else:
    #         print("\nNothing happens. Perhaps the clues in the paintings can help.")


def handle_command(com, pl, w, librarian):
    """Handle the move commands between each location. Check move status and move player accordingly.
    Call each location's handle function when current_location_index is updated. Handle all other commands."""
    current_location_index = w.map[pl.x][pl.y]
    librarian.check_spawn((pl.x, pl.y))

    command_parts = com.split()
    if len(command_parts) < 2 and 'move' in command_parts:
        print("Please specify a direction to move. Example: 'move north'")
        return True
    if com.startswith('move'):
        _, direction = com.split()
        if direction.lower() not in ['north', 'south', 'east', 'west']:
            print("Please specify a direction to move. Example: 'move north'")
            return True
        move_status, new_x, new_y = pl.move(direction, w.map)

        if move_status == "valid":
            location_index = w.map[new_x][new_y]

            new_location = w.locations[location_index]
            if new_location.unlocked:
                pl.x, pl.y = new_x, new_y
                print(new_location.long_description)
                if current_location_index in librarian.spawn_locations:
                    print("You're in a territory where a librarian can interact with you.")
            else:
                print("This location is locked. You can't enter yet.")
        else:
            print("You can't go that way or it's out of bounds.")

    elif command == 'quit':
        quit_game = input('Do you want to save your game? [y/n]')
        if quit_game == 'y':
            save_game(player, world)
        else:
            print("Game will not be saved.")
        return False  # Signal to exit the game loop

    elif command == 'help':
        print("Available commands: move [direction], quit, help, look, press")
    lib_index = w.map[pl.x][pl.y]
    librarian_present = lib_index in librarian.spawn_locations
    # Prioritize librarian interactions if present

    if librarian_present:
        if com.startswith('loot'):
            print("loot librarian")
            handle_librarian_interaction(com, pl, librarian, w)
            return True

    if current_location_index == 0:
        return handle_location0(com, pl, w)

    if current_location_index == 1:
        # Special handling for location 1
        return handle_location1(com, pl, w)

    if current_location_index == 2:
        return handle_location2(com, pl, w)

    if current_location_index == 3:
        return handle_location3(com, pl, w)

    # if current_location_index == 4:
    #     return handle_location4(command, player, world)
    return True


def print_progress_bar(word, duration=0.05, width=30):
    """Prints a simple progress bar in the console over a given duration of time."""
    for i in range(width + 1):
        percent = (i / width) * 100
        bar = '#' * i + '-' * (width - i)
        print(f"\r{word}: [{bar}] {percent: .2f}%", end="")
        time.sleep(duration / width)
    print()


def save_game(player, world, file_name='savegame.txt'):
    save_data = {
        'player_x': player.x,
        'player_y': player.y,
        'player_inventory': [item.name for item in player.inventory],
        'visited_locations': {loc_id: loc.visited for loc_id, loc in world.locations.items() if loc_id != -1}
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
    world.new_game = False

    for loc_id, visited in save_data['visited_locations'].items():
        if loc_id in world.locations:  # Only update if the location exists
            world.locations[loc_id].visited = visited
    print("Game loaded.")


if __name__ == "__main__":
    world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    player = Player(0, 0)
    librarian = Librarian(0, 0, "Librarian", ["book", "scroll"])
    print(librarian.spawn_locations)
    #new code

    start_choice = input("Do you want to 'start' a new game or 'load' saved game? ")
    if start_choice == 'load':
        try:
            load_game(player, world)
        except FileNotFoundError:
            print("No saved game found. Starting a new game.")
    if world.new_game == True:
        print("Welcome to the Text Adventure Game!")
        print("Rules and Regulations")
    else:
        print("Welcome BACK to Text Adventure Game!")
        print("same rules apply")

    s_short = 0.25
    time.sleep(s_short)
    player.set_location(0, 0)
    # print_progress_bar('Following Squirel', duration=5, width=30)
    world.locations[1].unlock()  # Unlock room 1 for testing
    world.locations[2].unlock()
    player.set_location(0, 2)
    #print(world.get_location(player.x, player.y).long_description)
    continue_game = True
    while continue_game:
        current_location = world.get_location(player.x, player.y)
        command = input(">> ").strip().lower()
        continue_game = handle_command(command, player, world, librarian)
        if command == 'look':
            if current_location:
                print(current_location.look())
            else:
                print("There's nothing to look at here.")
        elif command == 'item':
            print([item.name for item in world.get_location(player.x, player.y).items])
        elif command == 'inventory':
            player.show_inventory()
