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
                acquire(player, "ACORN")
                acquire(player, "Nail Shoe")
                return True
            else:
                print("Nothing happens. It seems to be the wrong code.")
        elif command == "quit":
            return False
        else:
            print("You are not sure what to do with that.")


#Location 2 - (Hallway with Painting)
def handle_location2(command, player, world):
    if command.startswith('talk'):
        if world.locations[3].unlocked:
            print("Talking with paintings won't solve more of your problems")
        else:
            return (paintings_hint(player, world))
    # else:
    #     print("Nothing interesting happens.")
    return True

def paintings_hint(player, world):
    current = 0
    """Move to the next paintings"""
    paintings = ["Painting 1 Clue", "Painting 2 Clue", "Painting 3 Clue", "Painting 4 Clue", "Painting 5 Clue"]
    world.locations[3].unlock()
    print(paintings[current + 1])
    return True


# Location 3 - (Horse Statue)
def handle_location3(command, player, world):
    if command == 'look':
        if world.locations[4].unlocked:
            print("The horse isn't here anymore.")
        else:
            return horse_statue_shoe(command, player, world)
    return True

def horse_statue_shoe(command, player, world):
    print("Hmmm... the horse's front left foot doesn't look quite right. It's missing something.")
    while True:
        inp = input(">> ").strip().lower()
        if len(inp.split()) >= 2:
            do, item = inp.split(' ', 1)
            if do == 'use':
                if item == 'nail shoe':
                    if item in [i.lower() for i in player.inventory]:
                        use_item(player, 'Nail Shoe')
                        horse_statue_read(command, player, world)
                    else:
                        print("You don't have that item yet. Come back again when you have it.")
                else:
                    if item in [i.lower() for i in player.inventory]:
                        print("This item cannot be used here.")
                    else:
                        print("You don't have that item.")
        elif inp == "use":
            print("Use what?")
        elif inp == "quit":
            return False
        elif inp == "inventory":
            print(player.inventory)
        elif inp.startswith("move"):
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")

def horse_statue_read(command, player, world):
    print("The horse's mouth opened up. Seems like something is in there.")
    while True:
        inp = input(">> ").strip().lower()
        if inp == 'look':
            print("There is a mystery letter in here. It reads ['astronomeeee']")
            print()
            print("The letter might be useful later on. You might want to keep it.")
            inp = input(">> ").strip().lower()
            while not inp.startswith('keep'):
                print("THE LETTER MIGHT BE USEFUL LATER ON. YOU MIGHT WANT TO KEEP IT")
                inp = input(">> ").strip().lower()
            acquire(player, "letter")
            horse_statue_go(command, player, world)
        elif inp == "quit":
            return False
        elif inp == "inventory":
            print(player.inventory)
        elif inp == "move":
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")

def horse_statue_go(command, player, world):
    print("Great! Now we have a letter. Oh wait.. The horse statue is moving!? To where? Let's mount on to see.")
    while True:
        inp = input(">> ").strip().lower()
        if inp == 'mount':
            world.locations[4].unlock()
            print("weeeee let's go!")
            print_progress_bar("riding the horse", duration=5, width=30)
            location_index = world.map[2][0]
            new_location = world.locations[location_index]
            player.x, player.y = 2, 0
            print(new_location.long_description)
        elif inp == "quit":
            return False
        elif inp == "inventory":
            print(player.inventory)
        elif inp == "move":
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")

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

    if current_location_index == 3:
        return handle_location3(command, player, world)

    # if current_location_index == 4:
    #     return handle_location4(command, player, world)
    return True



def print_progress_bar(word, duration=0.25, width=30):
    """Prints a simple progress bar in the console over a given duration of time."""
    for i in range(width + 1):
        percent = (i / width) * 100
        bar = '#' * i + '-' * (width - i)
        print(f"\r{word}: [{bar}] {percent:.2f}%", end="")
        time.sleep(duration / width)
    print()


def acquire(player, item):
    """Acquire the item, or add the item to player's inventory"""
    print(f" -- {item} has been acquired! Type 'inventory' to see. -- ")
    player.inventory.append(item)


def use_item(player, item):
    """Use the item and remove it from the pleyer's inventory"""
    print(f" -- {item} has been used. --")
    player.inventory.remove(item)

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
    print_progress_bar('Following Squirel', duration=5, width=30)
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
