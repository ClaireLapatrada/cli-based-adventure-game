"""The main adventure.py file. Click run on this file to start the game. """
import time
from game_data2 import World, Item, Location, Player, Librarian
import json


def handle_location0(com, pl, w):
    """Start location 0's events if it has not been cleared yet, else notify the player."""
    if not w.locations[1].unlocked:
        print("You see a squirrel next to your table, it looks like its calling you over. ")
        print("Type [follow squirrel]")
        com = input(">> ").strip().lower()
        while not com.startswith('follow squirrel'):
            print("Try again! Type [follow squirrel]")
            com = input(">> ").strip().lower()
        player.step_counts += 1
        print_progress_bar('Following Squirrel', duration=3, width=30)
        print(" ")
        w.locations[1].unlock()
        location_index = w.map[1][2]
        new_location = w.locations[location_index]
        # print(w.locations)
        player.set_location(1, 2)
        print(new_location.long_description)
    return True


# Location-1 (Vending) Helper Functions
def handle_location1(com, pl, w):
    """Start location 1's events if it has not been cleared yet, else notify the player."""
    global traded
    if not w.locations[2].unlocked:
        # Ensure the player interacts with the vending machine first
        # Handle the vending machine puzzle
        inp = input('Try inspecting the vending machine: type [vending]: ').strip().lower()
        while "vending" not in inp:
            inp = input('Try inspecting the vending machine by typing [vending], or learn to type!').strip().lower()
        player.step_counts += 1
        # Assuming passkey_vending is a function that handles the puzzle and unlocks the next location upon success
        passkey_vending(pl, w)
        print("\n You have successfully looted the vending machine! \n ")
        print("Another door appears... that seems to lead to another hallway east.")
        print("Only UofT Students are allowed in though, but you don't have your TCard. \n")
        # Handle the squirrel interaction
        inp = input('Try type [inspect squirrel]: ').strip().lower()
        while inp != 'inspect squirrel':
            player.step_counts += 1
            inp = input('Try type [inspect squirrel] to continue: ').strip().lower()

        print("\nThe squirrel seems to be holding your Tcard!"
              "Can you trade something that you have (it likes) for that Tcard?!\n")

    # Simplify by initializing the squirrel here with the trade items
    squirrel = Librarian(0, 0, 'Squirrel', [])
    squirrel.trade_items = ['Tcard']
    # squirrel.trade_items = ['Tcard', 'Chocolate']

    # Trade interaction loop
    while not traded:
        inp = input(">> ").strip().lower()
        if inp.startswith('trade '):
            player.step_counts += 1
            _, item = inp.split(' ', 1)
            if item.lower() == 'acorn' and 'Acorn' in [item.name for item in pl.inventory]:
                pl.check_use_item(item, 1)
                for item in world.get_location(player.x, player.y).items:
                    if item.name.lower() == 'tcard':
                        player.acquire(item)
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
    vending_machine = ['acorn', 'almond', 'peanut', 'cashew', 'pecan', 'horse shoe']
    print("\nThe squirrel is dancing around the machine, pointing to something inside that you can't figure out.")
    print("The vending machine has no slot for coins, only an alphanumeric keypad. It's probably free.")
    print(f"There's a variety of nuts sold here: {vending_machine}")
    print("\nType [type code] to select an item you want.\n")
    while True:
        inp = input(">> ").strip().lower()
        if inp.startswith("inspect"):
            player.step_counts += 1
            print("You inspect the vending machine closely.")
        elif inp == "type code":
            player.step_counts += 1
            code = input("Enter code: ").strip().lower()
            if code == "acorn":  # Replace with the actual code
                print("You hear a click sound as the next room is unlocked. \n")
                for item in w.get_location(pl.x, pl.y).items:
                    if item.name.lower() != 'tcard':
                        pl.acquire(item)
                return True
            else:
                print("Nothing happens. It seems to be the wrong code. Type [type code] to try again.")
        elif inp == "inventory":
            player.show_inventory()
        elif inp == 'interaction':
            print(f"You have {max_count - player.step_counts} interactions left before the exam starts!")
        elif inp == "hint":
            print(world.get_location(player.x, player.y).hint)
        elif inp == "help":
            print(world.get_location(player.x, player.y).valid_commands)
        elif inp == 'item':
            print(f"Available items here: {[item.name for item in world.get_location(player.x, player.y).items]}")
        elif inp.startswith("move"):
            player.step_counts += 1
            print("Why would you want to move away? There is something interesting here.")
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
        player.step_counts += 1
        if w.locations[3].unlocked:
            print("Talking with paintings won't solve more of your problems.")
        return paintings_hint()
    elif com == 'next':
        current_painting_index += 1
        return paintings_hint()
    elif com == "quit":
        return False
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
        player.step_counts += 1

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
        player.step_counts += 1
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
                player.step_counts += 1
                while not used:
                    used = player.check_use_item(item, 3, horse_statue_read, com, pl, w)
                    if used:
                        return True
                    else:
                        horse_statue_shoe(command, player, world)
                return True
        elif inp == "use":
            player.step_counts += 1
            print("Use what?")
        elif inp == "quit":
            return False
        elif inp == "inventory":
            player.show_inventory()
        elif inp == 'interaction':
            print(f"You have {max_count - player.step_counts} interactions left before the exam starts!")
        elif inp == "hint":
            print(world.get_location(player.x, player.y).hint)
        elif inp == "help":
            print(world.get_location(player.x, player.y).valid_commands)
        elif inp == 'item':
            print(f"Available items here: {[item.name for item in world.get_location(player.x, player.y).items]}")
        elif inp.startswith("move"):
            player.step_counts += 1
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
            player.step_counts += 1

            print("There is a mystery letter in here. It reads [It's ASTRONOMY, we're two worlds apart]")
            print()
            print("The letter might be useful later on. You might want to keep it.")
            inp = input(">> ").strip().lower()
            while not inp.startswith('keep'):
                print("THE LETTER MIGHT BE USEFUL LATER ON. YOU MIGHT WANT TO KEEP IT")
                inp = input(">> ").strip().lower()
            player.step_counts += 1
            for item in world.get_location(player.x, player.y).items:
                player.acquire(item)
            return horse_statue_go(command, player, world)
            # horse_statue_go(com, pl, w)
            # return True
        elif inp == "quit":
            return False
        elif inp == "inventory":
            player.show_inventory()
        elif inp == 'interaction':
            print(f"You have {max_count - player.step_counts} interactions left before the exam starts!")
        elif inp == "hint":
            print(world.get_location(player.x, player.y).hint)
        elif inp == "help":
            print(world.get_location(player.x, player.y).valid_commands)
        elif inp == 'item':
            print(f"Available items here: {[item.name for item in world.get_location(player.x, player.y).items]}")
        elif inp.startswith("move"):
            player.step_counts += 1
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")


def horse_statue_go(com, pl, w):
    """Ask user for the correct command, print progress bar for riding the horse,
    unlock and update new location as arrived. Print new location description. Handle all other commands."""
    print("Great! Now we have a letter. Oh wait.. The horse statue is moving!? To where? Let's MOUNT on to see.")
    while True:
        inp = input(">> ").strip().lower()
        if inp == 'mount':
            player.step_counts += 1
            world.locations[4].unlock()
            print("Weee let's go!")
            print_progress_bar("riding the horse", duration=5, width=30)
            location_index = world.map[4][1]
            new_location = world.locations[location_index]
            player.set_location(4, 1)
            print(new_location.long_description)
            return True
        elif inp == "quit":
            return False
        elif inp == "inventory":
            player.show_inventory()
        elif inp == 'interaction':
            print(f"You have {max_count - player.step_counts} interactions left before the exam starts!")
        elif inp == "hint":
            print(world.get_location(player.x, player.y).hint)
        elif inp == "help":
            print(world.get_location(player.x, player.y).valid_commands)
        elif inp == 'item':
            print(f"Available items here: {[item.name for item in world.get_location(player.x, player.y).items]}")
        elif inp.startswith("move"):
            player.step_counts += 1
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")


def handle_location4(com, pl, w):
    """Start location 4 events if it has not been cleared yet, else notify the player."""
    if com == 'take the elevator':
        player.step_counts += 1
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
                player.step_counts += 1

            print_progress_bar("On the elevator to 14th floor", duration=2, width=30)
            print("You have arrived on the rooftop. As you look around, you see a bunch of posters along the balcony.\n")
            print("Amongst the pile of posters, there is a suspicious looking black box with \n"
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
            player.step_counts += 1
            print("""
                         * Sirius
                           /
                    * Bellatrix     *
                           \\       /
                            *     *
                            |     |
                    *       *     *       *
                    Alnilam       Mintaka
                            \\     /
                             *   *
                            /     *
                           *       *
                         Saiph     Rigel
            """)

        elif inp == 'open box':
            player.step_counts += 1
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
                inp = input("Type 'acquire' to add the lucky pen to your inventory: ").strip().lower()
                while inp != 'acquire':
                    inp = input("Type 'acquire' to add the lucky pen to your inventory: ").strip().lower()
                for item in world.get_location(player.x, player.y).items:
                    player.acquire(item)
                letter = [i for i in player.inventory if i.name.lower() == 'letter'][0]
                player.remove_item(letter)
                print("Uhoh.. You dropped your letter. Oh well, you probably won't need it anymore."
                      "That took quite a lot of energy. It's time to refuel yourself up. "
                      "Let's head to the closest cafeteria.")
                world.locations[5].unlock()
                return True
            else:
                print()
                print("Some magic from the boxed pushed you out. That does not seems like the correct code. Try again.")
                print("To access the telescope, type 'telescope'. To access the black box, type 'open box'.")
        elif inp == "read letter":
            player.step_counts += 1
            print("astronomeee.")
        elif inp == "quit":
            return False
        elif inp == "inventory":
            player.show_inventory()
        elif inp == 'interaction':
            print(f"You have {max_count - player.step_counts} interactions left before the exam starts!")
        elif inp == "hint":
            print(world.get_location(player.x, player.y).hint)
        elif inp == "help":
            print(world.get_location(player.x, player.y).valid_commands)
        elif inp == 'item':
            print(f"Available items here: {[item.name for item in world.get_location(player.x, player.y).items]}")
        elif inp.startswith("move"):
            player.step_counts += 1
            print("Why would you want to move away? There is something interesting here.")
        else:
            print("You are not sure what to do with that.")


def handle_location5(com, pl, w):
    """Start location 5 events if it has not been cleared yet, else notify the player."""
    if not w.locations[6].unlocked:
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
        player.step_counts += 1

        # After eating, reveal the engraving
        print("As you finish your salad, you notice a small engraving at the bottom of the bowl: 'KJA'")

        # Puzzle interaction
        puzzle_input = input("Do you examine the engraving? (Hint: examine): ").strip().lower()
        if puzzle_input == "examine":
            player.step_counts += 1
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
        player.step_counts += 1


def handle_location6(com, pl, w):
    """Handle events at the Math Learning Center."""
    print("You enter the Math Learning Center and find a research assistant in need of help sorting papers.")

    # Check if the cheat sheet has already been found
    if 'Cheat Sheet' in [item.name for item in pl.inventory]:
        print("You have already found the cheat sheet. No need to sort more papers.")
        return True

    while True:
        inp = input("Type 'sort' to start sorting papers or 'leave' to exit: ").strip().lower()
        if inp == 'sort':
            player.step_counts += 1
            success = helper_sort()
            if success:
                # Simulate finding the cheat sheet after successful sorting
                for item in world.get_location(player.x, player.y).items:
                    player.acquire(item)
                print("As you sort the papers, you find the cheat sheet hidden among them!")
                # Call to flip blackboard after finding the cheat sheet
                flip_blackboard(com, pl, w)
                return False  # End the location event and game
            else:
                print("Game Over. You sorted the papers incorrectly too many times.")
                return False  # Signal game over or handle it appropriately
        elif inp == 'interaction':
            print(f"You have {max_count - player.step_counts} interactions left before the exam starts!")
        elif inp == "hint":
            print(world.get_location(player.x, player.y).hint)
        elif inp == "help":
            print(world.get_location(player.x, player.y).valid_commands)
        elif inp == 'item':
            print(f"Available items here: {[item.name for item in world.get_location(player.x, player.y).items]}")
        elif inp == 'leave':
            print("You decide to leave the Math Learning Center.")
            return True  # Player decides to leave without sorting
        else:
            print("Invalid command. Please type 'sort' to help or 'leave' to exit.")

# def handle_location6(com, pl, w):
#     """Handle events at the Math Learning Center."""
#     print("You enter the Math Learning Center and find a research assistant in need of help sorting papers.")
#     print("Help sort the papers correctly to find the cheat sheet.")
#
#     # Check if the cheat sheet has already been found
#     if 'Cheat Sheet' in [item.name for item in pl.inventory]:
#         print("You have already found the cheat sheet. No need to sort more papers.")
#         return True
#
#     while True:
#         inp = input("Type 'sort' to start sorting papers or 'leave' to exit: ").strip().lower()
#         if inp == 'sort':
#             success = helper_sort()
#             if success:
#                 # Simulate finding the cheat sheet after successful sorting
#                 cheat_sheet = Item('Cheat Sheet', 0, -1)  # Assuming -1 means it's not tied to a specific location
#                 pl.acquire(cheat_sheet)
#                 print("As you sort the papers, you find the cheat sheet hidden among them!")
#                 return True  # End the location event successfully
#             else:
#                 print("Game Over. You sorted the papers incorrectly too many times.")
#                 return False  # Signal game over or handle it appropriately
#         elif inp == 'leave':
#             print("You decide to leave the Math Learning Center.")
#             return True
#         else:
#             print("Invalid command. Please type 'sort' to help or 'leave' to exit.")


def helper_sort():
    """A helper function to simulate sorting Taylor Swift songs into the correct album piles."""
    albums_songs = {
        'Lover': 'Lover',
        'All Too Well (Taylor’s Version) (From The Vault)': 'Red (Taylor’s Version)',
        'Cardigan': 'Folklore',
        'Look What You Made Me Do': 'Reputation',
        'Wildest Dreams': '1989',
        'Shake It Off': '1989',
        'You Belong With Me': 'Fearless',
    }

    albums = {
        'Fearless': 1,
        '1989': 2,
        'Reputation': 3,
        'Folklore': 4,
        'Lover': 5,
        'Red (Taylor’s Version)': 6,
    }

    print("Here are the albums you can sort the songs into:")
    for album, pile in albums.items():
        print(f"Pile {pile}: {album}")

    mistakes = 0

    for song, correct_album in albums_songs.items():
        while True:
            print(f"\nSort the song '{song}' into the correct album pile: [1, 2, 3, 4, 5, 6]")
            try:
                inp = int(input("Pile number: "))
                if albums[correct_album] == inp:
                    print(f"'{song}' sorted correctly into '{correct_album}'.")
                    break
                else:
                    print("Incorrect album. Please try again.")
                    mistakes += 1
                    if mistakes == 3:
                        return False  # Too many mistakes, game over
            except ValueError:
                print("Please enter a valid number.")
            except KeyError:
                print("Invalid album choice. Please try again.")
    for item in world.get_location(player.x, player.y).items:
        player.acquire(item)
    return True


def flip_blackboard(com, pl, w):
    """
    A function to conclude the game by checking player's inventory, Tbucks, and offering a final message.
    """
    # Prompt for inventory check
    print("\nBefore you head to the exam center, let's make sure you have everything you need.")
    pl.show_inventory()

    # Conclude Tbucks and rank the player
    tbucks = pl.tbucks
    print(f"\nYou have {tbucks} Tbucks.")

    if tbucks >= 100:
        rank = "Gold"
    elif 50 <= tbucks < 100:
        rank = "Silver"
    else:
        rank = "Bronze"

    print(f"Based on your Tbucks, you've earned a {rank} Side Quest ranking!")

    # Flip the blackboard
    print("\nAs you prepare to leave, you notice something written on the blackboard.")
    flip = input("Flip the blackboard to read the message? (yes/no): ").strip().lower()

    if flip == "yes":
        player.step_counts += 1
        print("==========================================================================================")
        print("\nYou have successfully acquired all necessary items. Well done. Best of luck on the test.")
        print("\nRemember, it's the friends we made along the way that truly matter.")
        print("\nThank you for playing. Goodbye! \n")
        print("==========================================================================================")
    else:
        print("==========================================================================================")
        print("\nYou choose not to flip the blackboard, wondering what could have been written.")
        print("\nEither way, you feel prepared and ready for the test. Goodbye!")
        print("==========================================================================================")
    return False


def handle_librarian_interaction(com, pl, librarian, w):
    """ handle any interaction with the librarian. """
    if com.startswith('loot'):

        # Example trade logic
        print("Trade begins! Use commands like...\n"
              "[my inventory] : to check your Inventory \n"
              "[trade] : trade unused item for T-bucks, drop: to drop items \n"
              "[bargain] : to ask nicely for MORE T-bucks]\n"
              "[pity] : to Exit and leave librarian alone\n "
              "WARNING: after [pity] you cannot loot this poor soul again")
    while True:
        inp = input(">> ").strip().lower()
        if len(inp.split()) >= 2:
            do, item = inp.split(' ', 1)
            if do == 'trade':
                player.step_counts += 1
                librarian.trade_for_bucks(pl, item)
            elif do == 'my' and item == 'inventory':
                player.show_inventory()
            elif do.startswith('drop'):
                player.step_counts += 1
                print("drop logic #TODO")
            elif do.startswith('bargain'):
                player.step_counts += 1
                player.tbucks += 1
                print(player.tbucks)
            elif do.startswith('pity'):
                player.step_counts += 1
                librarian.interacted = True #pity()
                print("Libraian: Phew! Thank you for leaving me alone")
                time.sleep(0.02)
                print("Type 'look' to keep exploring the room")
                return False
        else:
            if inp == 'interaction':
                print(f"You have {max_count - player.step_counts} interactions left before the exam starts!")
            elif inp == "inventory":
                player.show_inventory()
            elif inp == "hint":
                print(world.get_location(player.x, player.y).hint)
            elif inp == "help":
                print(world.get_location(player.x, player.y).valid_commands)
            else:
                print(f"{inp} what? Be rigorous.")


def handle_command(com, pl, w, librarian):
    """Handle the move commands between each location. Check move status and move player accordingly.
    Call each location's handle function when current_location_index is updated. Handle all other commands."""
    global max_count
    current_location_index = w.map[pl.x][pl.y]
    #librarian.check_spawn((pl.x, pl.y))
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
                player.step_counts += 1
                location_index = w.map[new_x][new_y]
                new_location = w.locations[location_index]
                if new_location.unlocked:
                    librarian.interacted = False
                    pl.x, pl.y = new_x, new_y
                    current_location_index = w.map[pl.x][pl.y]
                    print(new_location.long_description)
                    w.locations[location_index].visited = True
                else:
                    print("This location is locked. You can't enter yet.")
            else:
                print("You can't go that way or it's out of bounds.")
    elif command == 'look':
        curr_location = w.get_location(pl.x, pl.y)
        if curr_location and curr_location.unlocked:
            print(curr_location.look())
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
    elif command == 'interaction':
        print(f"You have {max_count - player.step_counts} interactions left before the exam starts!")
    elif command == 'help':
        print(f"Available commands: {world.get_location(pl.x, pl.y).valid_commands}")
    elif command == 'hint':
        if world.locations[current_location_index + 1].unlocked:
            print("It's time to move on.")
        else:
            print(world.get_location(pl.x, pl.y).hint)

    lib_index = w.map[pl.x][pl.y]
    # print("before spawn")
    # print(lib_index in librarian.spawn_locations)
    # print(librarian.interacted)
    # librarian.check_spawn((pl.x, pl.y))
    # print("after spawn")
    librarian_present = lib_index in librarian.spawn_locations and not librarian.interacted
    if librarian_present:
        print("You're in a territory with a librarian that can trade with you. Type [loot] to begin trading.")
        if com.startswith('loot'):
            handle_librarian_interaction(com, pl, librarian, w)
            return True
    #
    # if librarian_present and not librarian.interacted:
    #     print("You're in a territory with a librarian that can traded. !Must Loot! Type [loot] to interact. ")
    #     if command.startswith('loot'):
    #         print("loot librarian")
    #         handle_librarian_interaction(command, pl, librarian, w)
    #         return True
    if player.step_counts > max_count:
        print("Game Over. The exam started. You didn't make it there on time.")
        return False
    elif player.step_counts + 1> max_count - 10:
        print(f"[WARNING] Be wise! You only have {max_count - player.step_counts + 1} more moves until the exam starts!")

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
    # Set up
    traded = False
    used = False
    max_count = 42
    # new code

    # start_choice = input("Do you want to 'start' a new game or 'load' saved game? ")
    # if start_choice == 'load':
    #     try:
    #         load_game(player, world)
    #     except FileNotFoundError:
    #         print("No saved game found. Starting a new game.")
    # if world.new_game:
    #     print("Welcome to the Text Adventure Game!")
    #     print("Rules and Regulations")
    # else:
    #     print("Welcome BACK to Text Adventure Game!")
    #     print("same rules apply")
    print("Welcome to Text Adventure Game!")
    start_choice = input("Type [Read Rules]: ")
    while start_choice.lower() != 'read rules':
        start_choice = input("Try Again! Type [Read Rules]: ")
    print("Game Objective: It's the morning of a big test, and you realize you've lost your three essential items: \n"
          "1. Your Lucky pen\n"
          "2. Cheat Sheet\n"
          "3. TCard \n"
          "Your mission is to navigate the world and 'acquire' these items in your inventory before the test begins.")
    print("-----------------")
    time.sleep(0.5)
    print("(*) General Commands:\n"
          "[quit]: Exit the game \n"
          "[move [direction]]: Move player in the specified direction \n"
          "[inventory]: Show player's inventory \n"
          "[look]: Print the brief description for player's current location \n"
          "[hint]: Provide game hints for each location \n"
          "[help]: Show all available commands in player's current location \n"
          "[interaction]: Show the number of interactions left before the exam starts \n"
          "[item]: Show all obtainable items in player's current location \n"
          "Notes: Some commands are not available while solving specific puzzles.")
    print("-----------------")
    time.sleep(0.6)
    print("(*) Interaction Limit: You have exactly 42 interactions.\n"
          "Each valid command you enter except the General Commands (see above), some event interactions, \n"
          "and input to the Final Challenge counts as one interaction. Choose wisely to avoid a premature game over! \n"
          "You can type 'help' to see the valid commands in each location.")
    print("-----------------")
    time.sleep(0.5)
    print("(*) Scoring: Throughout your quest, you'll earn Tbucks by completing side quests. Your prowess in acquiring \n"
          "Tbucks will determine your final rank: GOLD, SILVER, or BRONZE. \n"
          "To earn Tbucks, you must engage with the RANDOMLY SPAWNING LIBRARIANS, \n"
          "either by trading items or by bargaining for a extra Tbucks.")
    print("-----------------")
    time.sleep(0.40)
    print("(*) Final Challenge: In the last room, you are tasked with sorting critical information correctly. \n"
          "CAREFUL: You only get six attempts to place everything in its right place. Fail, and it's game over.")
    print("-------------")
    time.sleep(1)
    s_short = 0.25
    time.sleep(s_short)
    world.locations[0].unlock()
    player.set_location(1, 1)
    print(world.get_location(player.x, player.y).long_description)
    print("Try type [start] to embark on your adventure: ")

    # Testing Librian Trade
    # world.locations[6].unlock()
    # player.set_location(3, 0)

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
            print(f"Available items here: {[item.name for item in world.get_location(player.x, player.y).items]}")
        elif command == 'inventory':
            player.show_inventory()
