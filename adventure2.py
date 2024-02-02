"""The main adventure.py file. Click run on this file to start the game. """
import time
from game_data2 import World, Item, Location, Player, Librarian
import json


def handle_location0(com, pl, w):
    """Start location 0's events if it has not been cleared yet, else notify the player."""
    print("You wake up in your room and see a squirrel outside your window...")
    print("type 'follow squirrel'")
    com = input(">> ").strip().lower()
    while not com.startswith('follow'):
        print("do you need TYPING LESSSONS")
        com = input(">> ").strip().lower()
    print_progress_bar('Following Squirel', duration=3, width=30)
    w.locations[1].unlock()
    location_index = w.map[0][1]
    new_location = w.locations[location_index]
    player.set_location(0, 1)
    print(new_location.long_description)
    return True


# Location-1 (Vending) Helper Functions
def handle_location1(com, pl, w):
    """Start location 1's events if it has not been cleared yet, else notify the player."""
    global traded
    # Ensure the player interacts with the vending machine first
    # Handle the vending machine puzzle
    if not w.locations[2].unlocked:
        inp = input('Try inspecting the vending machine: type [vending]: ').strip().lower()
        while "vending" not in inp:
            inp = input('Try inspecting the vending machine by typing [vending], or learn to type!').strip().lower()

        # Assuming passkey_vending is a function that handles the puzzle and unlocks the next location upon success
        passkey_vending(pl, w)
        print(
            "You have successfully looted the vending machine! \nAnother door appears... that seems to lead to another hallway east.\nOnly UofT Students are allowed in though, but you don't have your TCard.")

        # Handle the squirrel interaction
        inp = input('Try type [inspect squirrel]: ').strip().lower()
        while inp != 'inspect squirrel':
            inp = input('Try type [inspect squirrel] to continue: ').strip().lower()

        print(
            "The squirrel seems to be holding your Tcard!\nCan you trade something that you have (it likes) for that Tcard?!")

    # Simplify by initializing the squirrel here with the trade items
    squirrel = Librarian(0, 0, 'Squirrel', [])
    squirrel.trade_items = ['Tcard', 'Chocolate']

    # Trade interaction loop
    while not traded:
        inp = input(">> ").strip().lower()
        if inp.startswith('trade '):
            _, item = inp.split(' ', 1)
            if item.lower() == 'acorn' and 'Acorn' in [item.name for item in pl.inventory]:
                pl.check_use_item(item, 1)
                pl.acquire(Item('Tcard', -1, 8))  # Simulate acquiring TCard
                print("You traded an acorn for the Tcard. The squirrel scampers away happily.")
                w.locations[2].unlock()  # Unlock next location
                traded = True  # Set the flag to True to exit loop
            else:
                print(f"The squirrel doesn't seem interested in {item}. Try trading something else.")
        elif inp == "quit":
            return False
        elif inp == "inventory":
            pl.show_inventory()
        else:
            print("To trade with the squirrel, type 'trade [item]'.")

    exit = ""
    return traded  # Return the status of the trade


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
                # Assuming location 2 is the next one
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
    """Start location 3 events if it has not been cleared yet, else notify the player."""
    if com == 'inspect':
        if w.locations[4].unlocked:
            print("The horse isn't here anymore.")
        else:
            print("Hmmm... the horse's front left foot doesn't look quite right. It's missing something.")
            return horse_statue_shoe(com, pl, w)
    return True


def horse_statue_shoe(com, pl, w):
    """Ask player for input to use the horse shoe, call horse_statue_read() once the correct item has been used.
    Handle all other commands."""
    global used
    while not used:
        inp = input(">> ").strip().lower()
        if len(inp.split()) >= 2:
            do, item = inp.split(' ', 1)
            if do == 'use':
                while not used:
                    used = player.check_use_item(item, 3, horse_statue_read, com, pl, w)
                    if used:
                        return True
                    else:
                        horse_statue_shoe(command, player, world)
                return True
        elif inp == "use":
            print("Use what?")
        elif inp == "quit":
            return False
        elif inp == "inventory":
            player.show_inventory()
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
            for item in world.get_location(player.x, player.y).items:
                player.acquire(item)
            return horse_statue_go(command, player, world)
            # horse_statue_go(com, pl, w)
            # return True
        elif inp == "quit":
            return False
        elif inp == "inventory":
            player.show_inventory()
        elif inp.startswith("move"):
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
            world.locations[4].unlock()
            print("weeeee let's go!")
            print_progress_bar("riding the horse", duration=5, width=30)
            location_index = world.map[2][0]
            new_location = world.locations[location_index]
            player.set_location(2, 0)
            print(new_location.long_description)
            return True
        elif inp == "quit":
            return False
        elif inp == "inventory":
            player.show_inventory()
        elif inp.startswith("move"):
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")


# TODO
def handle_location4(com, pl, w):
    """Start location 4 events if it has not been cleared yet, else notify the player."""
    if com == 'take the elevator':
        if w.locations[5].unlocked:
            print("It's already morning. The rooftop is closed.")
        else:
            floor = input("Floor: ")
            while floor != "14":
                if floor.isnumeric() and int(floor) < 14 and int(floor) >= 1:
                    print(f"Floor {floor} is closed right now.")
                else:
                    print("Invalid input, please try again.")
                floor = input("Floor: ")

            print_progress_bar("On the elevator to 14th floor", duration=2, width=30)
            print("You have arrived on the rooftop. As you look around, you see a bunch of posters along the balcony.")
            print("Amongst the pile of posters, there is a suspicious looking black box with "
                  "'lenx' carved at the front.")
            print("Luckily, the telescope is right in front of you.")
            return stars_puzzle(com, pl, w)
    return True


def stars_puzzle(com, pl, w):
    """ Print out stars and repeat prompts until user input the correct pin on the pin pad. """
    solution = "697655"
    print("To access the telescope, type 'telescope'. To access the black box, type 'open box'.")
    while True:
        inp = input(">> ").strip().lower()
        if inp == 'telescope':
            print("""
             * Sirius
               /
        * Bellatrix     *
               \       /
                *     *
                |     |
        *       *     *       *
        Alnilam       Mintaka
                \     /
                 *   *
                /     *
               *       *
             Saiph     Rigel
            """)
        elif inp == 'open box':
            print("LENX")
            print("The pin pad only accepts 6-digits of numbers from 0-9.")
            print("_ _ _ _ _ _")
            user_input = input(">> ").strip()

            display = ['_', '_', '_', '_', '_', '_']
            for i, char in enumerate(user_input):
                if i < len(display):
                    display[i] = char
                    print("\r" + " ".join(display), end="")
                    time.sleep(0.5)

            # Check the solution after the animation
            if user_input == solution:
                # Animation for revealing each letter

                print("\nThe box clicks open, you find a magic looking pen in it.")
                inp = input("Type 'acquire' to add the magic pen to your inventory: ").strip().lower()
                while inp != 'acquire':
                    inp = input("Type 'acquire' to add the magic pen to your inventory: ").strip().lower()
                for item in w.get_location(pl.x, pl.y).items:
                    pl.acquire(item)
                print("Uhoh.. That took quite a lot of energy. It's time to refuel yourself up. "
                      "Let's head to the closest cafeteria.")
                world.locations[5].unlock()
                return True
            else:
                print()
                print("Some magic from the boxed pushed you out. That does not seems like the correct code. Try again.")
                print("To access the telescope, type 'telescope'. To access the black box, type 'open box'.")
        elif inp == "read letter":
            print("astronomeee.")
        elif inp == "quit":
            return False
        elif inp == "inventory":
            player.show_inventory()
        elif inp.startswith("move"):
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")


def handle_location5(com, pl, w):
    """Start location 5 events if it has not been cleared yet, else notify the player."""
    print("You're in Sid Smith, everything is closed except for a new shop called 'TwoGreens'. "
          "What a weird name, but you need your calories.")

    # Initialize caesar to False
    caesar = False

    while not caesar:
        salad_choice = input("Choose your salad [Caesar salad, Greek salad, Chef's salad]: ")
        # Check if the choice is Caesar salad
        if salad_choice.lower() == "caesar salad":
            print("Ah, a choice of a true CS major. Caesar always #chr(ord(m)-k)) forever.")
            caesar = True
        elif salad_choice.lower() not in ["caesar salad", "greek salad", "chef's salad"]:
            print("That's not a valid choice, please choose from the menu.")
        else:
            print("Are you really a CS major?? Caesar always #chr(ord(m)-k)) forever.")
            # If you want to give the user another chance regardless of their choice,
            # you could remove the 'caesar = True' or adjust the logic accordingly.
            # If the purpose is to keep asking until Caesar salad is selected, then the code is fine.
            # Otherwise, to proceed with any valid choice, you could set 'caesar = True' here as well.

    # Proceed with the next steps after making a choice

    # Eat interaction
    eat_action = input("What will you do with the salad? (Hint: eat): ").strip().lower()
    if eat_action != "eat":
        print("What are you gonna do, BREATHE it?")
        return True

    # Simulate eating with a progress bar
    print("You start eating the salad...")
    print_progress_bar("Eating", duration=5, width=30)

    # After eating, reveal the engraving
    print("As you finish your salad, you notice a small engraving at the bottom of the bowl: 'KJA'")

    # Puzzle interaction
    puzzle_input = input("Do you examine the engraving? (Hint: examine): ").strip().lower()
    if puzzle_input == "examine":
        puzzle_caesar_salad(pl, w)
    else:
        print("You decide not to examine the engraving. Maybe next time.")

    return True


def puzzle_caesar_salad(pl, w):
    """Activate the Caesar Salad puzzle, wait until player input the right answer."""
    print("The engraving 'KJA' seems to be a hint. It's followed by '+ 2'. Hmm, a Caesar cipher perhaps?")

    # Correct solution according to the Caesar cipher hint
    solution = "mlc"  # Lowercase for consistent comparison

    while True:
        print("\nYou stand before a door with no handles, only a panel with letters.")
        print("_ _ _")
        user_input = input(">> ").strip().lower()

        # Check if the user wants to quit before processing further
        if user_input == "quit":
            print("\nQuitting the puzzle.")
            return False

        # Prepare display for animation
        display = ['_', '_', '_']
        for i, char in enumerate(user_input):
            if i < len(display):
                display[i] = char
        print("\r" + " ".join(display))  # Print the final state of display after input
        time.sleep(0.5)  # Wait a bit before checking the solution

        # Check the solution
        if user_input == solution:
            print("\nThe door clicks open, revealing a new path ahead.")
            w.locations[6].unlock()
            return True
        else:
            print("\nNothing happens. Perhaps the clues at the bottom of the salad bowl can help.")


def handle_location6(com, pl, w):
    """Start location 6 events if it has not been cleared yet, else notify the player."""
    pass


def handle_librarian_interaction(com, pl, librarian, w):
    """ handle any interaction with the librarian. """
    # print("you're in a territory with a librarian that can trade with you")
    if com.startswith('loot'):
        # Example trade logic
        print("Trade begins: use command like\n"
              "[trade: trade unused item for Tbucks, drop: to drop items, bargain: to ask nicely for MORE Tbucks]\n"
              "[pity: leave the poor librian alon WARNING: you cannot loot this poor soul again")
    while True:
        inp = input(">> ").strip().lower()
        if len(inp.split()) >= 2:
            do, item = inp.split(' ', 1)
            if do == 'trade':
                librarian.trade_for_bucks(pl, item)
            elif do.startswith('drop'):
                print("drop logic #TODO")
            elif do.startswith('bargain'):
                player.tbucks += 1
                print(player.tbucks)
            elif do.startswith('pity'):
                print("Libraian: Phew! Thank you for leaving me alone")
                time.sleep(0.02)
                print("Type 'look' to keep exploring the room")
                return False
        else:
            print(f"{inp} what? Be rigorous.")


def handle_command(com, pl, w, librarian):
    """Handle the move commands between each location. Check move status and move player accordingly.
    Call each location's handle function when current_location_index is updated. Handle all other commands."""
    current_location_index = w.map[pl.x][pl.y]
    librarian.check_spawn((pl.x, pl.y))
    command_parts = command.split()

    if len(command_parts) < 2 and 'move' in command_parts:
        print("Please specify a direction to move. Example: 'move north'")
        return True
    if command.startswith('move'):
        _, direction = command.split()
        if direction.lower() not in ['north', 'south', 'east', 'west']:
            print("Please specify a direction to move. Example: 'move north'")
        else:
            move_status, new_x, new_y = pl.move(direction, w.map)

            if move_status == "valid":
                location_index = w.map[new_x][new_y]

                new_location = w.locations[location_index]
                if new_location.unlocked:
                    pl.x, pl.y = new_x, new_y
                    current_location_index = w.map[pl.x][pl.y]
                    # print(pl.x)
                    # print(pl.y)
                    print(new_location.long_description)
                else:
                    print("This location is locked. You can't enter yet.")
            else:
                print("You can't go that way or it's out of bounds.")
    elif com == 'look':
        current_location = w.get_location(pl.x, pl.y)
        if current_location and current_location.unlocked:
            print(current_location.look())
        else:
            print("There's nothing to look at here.")
        return True
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
        if command.startswith('loot'):
            print("loot librarian")
            handle_librarian_interaction(command, pl, librarian, w)
            return True

    if current_location_index == 0:
        return handle_location0(command, player, world)

    if current_location_index == 1:
        return handle_location1(command, player, world)

    if current_location_index == 2:
        return handle_location2(command, player, world)

    if current_location_index == 3:
        return handle_location3(command, player, world)

    if current_location_index == 4:
        return handle_location4(command, player, world)

    if current_location_index == 5:
        return handle_location5(command, player, world)

    if current_location_index == 6:
        return handle_location6(command, player, world)
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
    """Save current game data in a file with the given filename."""
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
    """Load game from savegame.txt"""
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
    # Set up
    traded = False  # Flag to check if trade was successful
    used = False

    # new code

    start_choice = input("Do you want to 'start' a new game or 'load' saved game? ")
    if start_choice == 'load':
        try:
            load_game(player, world)
        except FileNotFoundError:
            print("No saved game found. Starting a new game.")
    if world.new_game:
        print("Welcome to the Text Adventure Game!")
        print("Rules and Regulations")
    else:
        print("Welcome BACK to Text Adventure Game!")
        print("same rules apply")

    s_short = 0.25
    time.sleep(s_short)
    player.set_location(0, 0)
    print(world.get_location(player.x, player.y).long_description)

    # Testing Librian Trade
    # world.locations[5].unlock()
    # player.set_location(1, 0)
    # print(player.x)
    # print(world.map[player.x][player.y])
    # print(world.map)
    # world.locations[2].unlock()
    # player.set_location(0, 2)
    # player.inventory +=

    continue_game = True
    while continue_game:
        current_location = world.get_location(player.x, player.y)
        command = input(">> ").strip().lower()
        continue_game = handle_command(command, player, world, librarian)
        # if command == 'look':
        #     if current_location:
        #         print(current_location.look())
        #     else:
        #         print("There's nothing to look at here.")
        if command == 'item':
            print([item.name for item in world.get_location(player.x, player.y).items])
        elif command == 'inventory':
            player.show_inventory()
