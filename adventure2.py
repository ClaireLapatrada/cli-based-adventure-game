import time
from game_data2 import World, Item, Location, Player

#Location-1 (Vending) Helper Functions
def handle_location1(command, player, world):
    if "vending" in command:
        if world.locations[2].unlocked:
            print("Vending Machine Puzzle has been solved. No other useful clues. ")
        else:
            return passkey_vending(player, world)
    # else:
    #     print("Nothing interesting happens.")
    return True

def passkey_vending(player, world):
    print("The vending machine has no slot for coins, only an alphanumeric keypad.")
    while True:
        command = input(">> ").strip().lower()
        if command.startswith("inspect"):
            print("You inspect the vending machine closely.")
        elif command == "type code":
            code = input("Enter code: ").strip()
            if code == "correct_code":  # Replace with the actual code
                print("You hear a click sound as the next room is unlocked.")
                world.locations[2].unlock()  # Assuming location 2 is the next one
                print(" -- ACORN and TCARD has been acquired! Type 'inventory' to see. -- ")
                player.inventory.append("ACORN")
                player.inventory.append("TCARD")
                return True
            else:
                print("Nothing happens. It seems to be the wrong code.")
        elif command == "quit":
            return False
        else:
            print("You are not sure what to do with that.")


#Location 2 - (Hallway with Painting)
current_painting_index = 0

def handle_location2(command, player, world):
    global current_painting_index

    if command == 'talk':
        if world.locations[3].unlocked:
            print("Talking with paintings won't solve more of your problems.")
        else:
            return paintings_hint(player, world)
    elif command == 'next':
        current_painting_index += 1
        return paintings_hint(player, world)
    else:
        print("You can't do that here.")

    return True

def paintings_hint(player, world):
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
        return door_puzzle(player, world)
    return True

def door_puzzle(player, world):
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

def handle_command(command, player, world):
    current_location_index = world.map[player.x][player.y]
    command_parts = command.split()
    if len(command_parts) < 2 and 'move' in command_parts:
        print("Please specify a direction to move. Example: 'move north'")
        return True
    if command.startswith('move'):
        _, direction = command.split()
        if direction.lower() not in ['north', 'south', 'east', 'west']:
            print("Please specify a direction to move. Example: 'move north'")
            return True
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

    if current_location_index == 1:
        # Special handling for location 1
        return handle_location1(command, player, world)

    if current_location_index == 2:
        return handle_location2(command, player, world)

    return True



def print_progress_bar(word, duration=0.05, width=30):
    """Prints a simple progress bar in the console over a given duration of time."""
    for i in range(width + 1):
        percent = (i / width) * 100
        bar = '#' * i + '-' * (width - i)
        print(f"\r{word}: [{bar}] {percent:.2f}%", end="")
        time.sleep(duration / width)
    print()



if __name__ == "__main__":
    world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    player = Player(0, 0)

    s_short = 0.25
    print("Welcome to the Text Adventure Game!")
    print("Rules and Regulations")
    time.sleep(s_short)

    print("You wake up in your room and see a squirrel outside your window...")
    print("type 'follow squirrel'")
    command = input(">> ").strip().lower()
    while not command.startswith('follow'):
        print("do you need TYPING LESSSONS")
        command = input(">> ").strip().lower()
    #print_progress_bar('Following Squirel', duration=5, width=30)
    world.locations[1].unlock()  # Unlock room 1 for testing
    player.set_location(0, 1)
    print(world.get_location(player.x, player.y).long_description)
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
        elif command == 'inventory':
            print(player.inventory)
