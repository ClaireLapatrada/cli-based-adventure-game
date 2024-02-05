"""The main adventure.py file. Click run on this file to start the game. """
import time
from typing import Optional
from game_data import World, Player, Librarian


def handle_location0(local_world: World, local_player: Player) -> Optional:
    """Start location 0's events if it has not been cleared yet, else notify the player."""
    if not local_world.locations[1].unlocked:
        print("You see a squirrel next to your table, it looks like its calling you over. ")
        print("Type [follow squirrel]")
        com = input(">> ").strip().lower()
        while not com.startswith('follow squirrel'):
            print("Try again! Type [follow squirrel]")
            com = input(">> ").strip().lower()
        local_player.step_counts += 1
        print_progress_bar('Following Squirrel ', duration=3, width=30)
        print(" ")
        local_world.locations[1].unlock()
        location_index = local_world.map[1][2]
        new_location = local_world.locations[location_index]
        local_player.set_location(1, 2)
        print(new_location.long_description)

    return True


# Location-1 (Vending) Helper Functions
def handle_location1(local_world: World, local_player: Player, local_traded: bool) -> Optional:
    """Start location 1's events if it has not been cleared yet, else notify the player."""
    if not local_world.locations[2].unlocked:
        # Ensure the player interacts with the vending machine first
        inp = input('Try inspecting the vending machine: type [vending]: ').strip().lower()
        while "vending" not in inp:
            inp = input('Try inspecting the vending machine by typing [vending], or learn to type!').strip().lower()
        local_player.step_counts += 1
        # Assuming passkey_vending is a function that handles the puzzle and unlocks the next location upon success
        passkey_vending(local_world, local_player)
        print("\n You have successfully looted the vending machine! \n ")
        print("Another door appears... that seems to lead to another hallway east.")
        print("Only UofT Students are allowed in though, but you don't have your TCard. \n")
        # Handle the squirrel interaction
        inp = input('Try type [inspect squirrel]: ').strip().lower()
        if inp == "inventory":
            local_player.show_inventory()
        while inp != 'inspect squirrel':
            local_player.step_counts += 1
            inp = input('Try type [inspect squirrel] to continue: ').strip().lower()

        print("The squirrel seems to be holding your Tcard! "
              "Can you trade something that you have (it likes) for that Tcard?!\n")

    squirrel = Librarian(0, 0, 'Squirrel')
    squirrel.trade_items = ['Tcard']

    # Trade interaction loop
    while not local_traded:
        inp = input(">> ").strip().lower()
        if inp in actions:
            actions[inp]()
        elif inp.startswith('trade '):
            local_player.step_counts += 1
            _, item = inp.split(' ', 1)
            if item.lower() == 'acorn' and 'Acorn' in [it.name for it in player.inventory]:
                print("You traded an acorn for the Tcard.")
                local_player.check_use_item(item, 1)
                acquire_only(local_world, local_player, 'tcard')
                local_player.tbucks += 500
                print("\n -- You have been gifted 500 Tbucks for obtaining the required item! -- \n\n"
                      "The squirrel scampers away happily.")
                local_world.locations[2].unlock()
                local_traded = True
            else:
                print(f"The squirrel doesn't seem interested in {item}. Try trading something else.")
        else:
            print("To trade with the squirrel, type 'trade [item]'.")
    return local_traded  # Return the status of the trade


def passkey_vending(local_world: World, local_player: Player) -> Optional:
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
                acquire_all_except(local_world, local_player, 'tcard')
                return True
            else:
                print("Nothing happens. It seems to be the wrong code. Type [type code] to try again.")
        elif inp in actions:
            actions[inp]()
        else:
            print("You are not sure what to do with that.")


# Location 2 - (Hallway with Painting)
def handle_location2(local_command: str, local_world: World) -> Optional:
    """Start location 2's events if it has not been cleared yet, else notify the player."""
    global current_painting_index
    if local_command == 'talk':
        player.step_counts += 1
        if local_world.locations[3].unlocked:
            print("Talking with paintings won't solve more of your problems.")
        else:
            return paintings_hint(local_world)
    elif local_command == 'next':
        current_painting_index = current_painting_index + 1
        return paintings_hint(local_world)
    elif local_command == "quit":
        return False
    # else:
    #     print("You can't do that here.")
    return True


def paintings_hint(local_world: World) -> Optional:
    """Move to the next painting and call the door puzzle onve all paintings have been visited.
    Handle all other commands."""
    global current_painting_index
    paintings = [
        "Get ready to receive words of wisdom from the paintings. Type [next] to keep talking.",
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
        return door_puzzle(local_world)
    return True


def door_puzzle(local_world: World) -> Optional:
    """Ask user for input to the door puzzle, with animation when revealing the correct code.
    Handle all other commands."""
    solution = "secret"
    while True:
        print("\nYou stand before a door with no handles, only a panel with letters.")
        print("_ _ _ _ _ _")
        user_input = input(">> ").strip().lower()
        player.step_counts += 1
        # Animation for revealing each letter
        blank_lines(user_input, 6)
        # Check the solution after the animation
        if user_input == solution:
            print("\nThe door clicks open, revealing a new path ahead.")
            local_world.locations[3].unlock()
            return True
        elif user_input == "quit":
            print("\nQuitting the puzzle.")
            return False
        else:
            print("\nNothing happens. Perhaps the clues in the paintings can help.")


# Location 3 - (Horse Statue)
def handle_location3(local_command: str, local_world: World, local_player: Player,
                     local_used: bool) -> Optional:
    """Start location 3 events if it has not been cleared yet, else notify the player."""
    if local_command == 'inspect':
        local_player.step_counts += 1
        if local_world.locations[4].unlocked:
            print("The horse isn't here anymore.")
        else:
            print("Hmmm... the horse's front left foot doesn't look quite right. It's missing something."
                  " Perhaps you can [use] something you have on it?")
            return horse_statue_shoe(local_world, local_player, local_used)
    return True


def horse_statue_shoe(local_world: World, local_player: Player, local_used: bool) -> Optional:
    """Ask the player for input to use the horse shoe, call horse_statue_read() once the correct item has been used.
    Handle all other commands."""
    while not local_used:
        inp = input(">> ").strip().lower()
        if len(inp.split()) < 2 and inp == "use":
            local_player.step_counts += 1
            print("Use what?")
        elif len(inp.split()) < 2 and inp in actions:
            actions[inp]()
        elif len(inp.split()) < 2:
            print("You are not sure what to do with that.")
        elif len(inp.split()) >= 2 and inp.split()[0] == 'use':
            _, item = inp.split(' ', 1)
            local_player.step_counts += 1
            read = horse_statue_read(local_world, local_player)
            local_used = local_player.check_use_item(item, 3, read)
            if local_used:
                return True
            else:
                horse_statue_shoe(local_world, local_player, local_used)
                return True
        else:
            print("You are not sure what to do with that.")
    return True


def horse_statue_read(local_world: World, local_player: Player) -> Optional:
    """Ask player for the right command to inspect the letter and keep it, call horse_statue_go when completed.
    Handle all other commands."""
    print("The horse's mouth opened up. Seems like something is in there.")
    while True:
        inp = input(">> ").strip().lower()
        if inp == 'inspect':
            player.step_counts += 1

            print("There is a mystery letter in here with a bunch of other stuff. "
                  "The letter reads [It's ASTRONOMY, we're two worlds apart]")
            print("These items might be useful later on. You might want to [keep] it.")
            inp = input(">> ").strip().lower()
            while not inp.startswith('keep'):
                print("THE LETTER MIGHT BE USEFUL LATER ON. YOU MIGHT WANT TO [KEEP] IT")
                inp = input(">> ").strip().lower()
            player.step_counts += 1
            acquire_all_except(local_world, local_player)
            return horse_statue_go(local_world)
        elif inp in actions:
            actions[inp]()
        else:
            print("You are not sure what to do with that.")


def horse_statue_go(local_world: World) -> Optional:
    """Ask user for the correct command, print progress bar for riding the horse,
    unlock and update new location as arrived. Print new location description. Handle all other commands."""
    print("Amazing! The horse gave you extra items from its saddle bag - kept for trading later!\n"
          "Oh wait.. The horse statue is moving!? To where? Let's [mount] on to see.")
    while True:
        inp = input(">> ").strip().lower()
        if inp == 'mount':
            player.step_counts += 1
            local_world.locations[4].unlock()
            print("Weee let's go!")
            print_progress_bar("riding the horse ", duration=5, width=30)
            location_index = local_world.map[4][1]
            new_location = local_world.locations[location_index]
            player.set_location(4, 1)
            print(new_location.long_description)
            return True
        elif inp in actions:
            actions[inp]()
        else:
            print("You are not sure what to do with that.")


def handle_location4(local_command: str, local_world: World, local_player: Player) -> Optional:
    """Start location 4 events if it has not been cleared yet, else notify the player."""
    if local_command == 'take the elevator' and local_world.locations[5].unlocked:
        local_player.step_counts += 1
        print("It's already morning. The rooftop is closed.")
    elif local_command == 'take the elevator':
        floor = input("Floor: ")
        while floor != "14":
            if floor.isnumeric() and int(floor) < 14 and int(floor) >= 1:
                print(f"Floor {floor} is closed right now.")
            else:
                print("Invalid input, please try again.")
            floor = input("Floor: ")
            local_player.step_counts += 1

        print_progress_bar("On the elevator to 14th floor ", duration=2, width=30)
        print("You have arrived on the rooftop. As you look around, you see a pile of posters along the balcony.\n")
        print("Amongst the pile of posters, there is a suspicious looking black box with \n"
              "'lenx' carved at the front.")
        print("Luckily, the telescope is right in front of you.")
        return stars_puzzle(local_world, local_player)
    return True


def stars_puzzle(local_world: World, local_player: Player) -> Optional:
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

            blank_lines(user_input, 6)
            if check_stars_puzzle(user_input, solution, local_world, local_player):
                return True

        elif inp == "read letter":
            player.step_counts += 1
            print("The letter reads [It's ASTRONOMY, we're two worlds apart]")
        elif inp in actions:
            actions[inp]()
        else:
            print("You are not sure what to do with that.")


def check_stars_puzzle(user_input: str, solution: str, local_world: World, local_player: Player) -> bool:
    """Helper function for checking the answer for stars puzzle"""
    # Check the solution after the animation
    if user_input == solution:
        # Animation for revealing each letter
        print("\nYes! Each number corresponds to the length of each Star's name!")
        print("\nThe box clicks open, you find a magic looking pen in it.")
        inp = input("Type 'acquire' to add the lucky pen to your inventory: ").strip().lower()
        while inp != 'acquire':
            inp = input("Type 'acquire' to add the lucky pen to your inventory: ").strip().lower()
            print()
        acquire_all_except(local_world, local_player)
        player.tbucks += 500
        print("-- You have been gifted 500 Tbucks for obtaining the required item -- \n")
        print("That took quite a lot of energy. It's time to refuel yourself up. "
              "Let's [go] to the closest cafeteria.")
        local_world.locations[5].unlock()
        return True
    else:
        print()
        print("Some magic from the boxed pushed you out. That does not seems like the correct code. Try again.")
        print("To access the telescope, type 'telescope'. To access the black box, type 'open box'.")
        return False


def handle_location5(local_world: World, local_player: Player) -> Optional:
    """Start location 5 events if it has not been cleared yet, else notify the player."""
    if not local_world.locations[6].unlocked:
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

        # Proceed with the next steps after making a choice

        # Eat interaction
        eat_action = input("What will you do with the salad? (Hint: eat): ").strip().lower()
        while eat_action != "eat":
            eat_action = input("Try again! Comsume the salad. : ").strip().lower()

        # Simulate eating with a progress bar
        print("You start eating the salad...")
        print_progress_bar("Eating ", duration=5, width=30)
        local_player.step_counts += 1

        # After eating, reveal the engraving
        print("As you finish your salad, you notice a small engraving at the bottom of the bowl: 'KJA'")

        # Puzzle interaction
        puzzle_input = input("Try take a closer look at the engraving ").strip().lower()
        while puzzle_input != "examine":
            puzzle_input = input("Try [examine] the engraving ")
        if puzzle_input == "examine":
            player.step_counts += 1
            puzzle_caesar_salad(local_world)
        else:
            print("You decide not to examine the engraving, what?")

    return True


def puzzle_caesar_salad(local_world: World) -> Optional:
    """Activate the Caesar Salad puzzle, wait until player input the right answer."""
    print("The engraving 'KJA' seems to be a hint. It's followed by '+ 2'. Hmm, a Caesar cipher perhaps?")

    # Correct solution according to the Caesar cipher hint
    solution = "mlc"  # Lowercase for consistent comparison

    while True:
        print("\nA pink portal appeared before you, on it is a panel with letters.")
        print("_ _ _")
        user_input = input(">> ").strip().lower()

        # Check if the user wants to quit before processing further
        if user_input == "quit":
            print("\nQuitting the puzzle.")
            return False

        blank_lines(user_input, 3)

        # Check the solution
        if user_input == solution:
            print("\nThe pink portal opens up, revealing a new path ahead. Let's [go] out!")
            local_world.locations[6].unlock()
            return True
        else:
            print("\nNothing happens. Perhaps the clues at the bottom of the salad bowl can help.")
        player.step_counts += 1


def handle_location6(local_world: World, local_player: Player) -> Optional:
    """Handle events at the Math Learning Center."""
    print("You enter the Math Learning Center and find a research assistant in need of help sorting papers.")

    # Check if the cheat sheet has already been found
    if 'Cheat Sheet' in [it.name for it in local_player.inventory]:
        print("You have already found the cheat sheet. No need to sort more papers.")
        return True

    while True:
        inp = input("Type 'sort' to start sorting papers: ").strip().lower()
        if inp == 'sort':
            local_player.step_counts += 1
            success = helper_sort()
            if success:
                found_cheatsheet(local_world, local_player)
                return False  # End the location event and game
            else:
                print("Game Over. You sorted the papers incorrectly too many times.")
                return False  # Signal game over or handle it appropriately
        elif inp in actions:
            actions[inp]()
        else:
            print("Invalid command. Please type 'sort' to help:")


def found_cheatsheet(local_world: World, local_player: Player) -> None:
    """A helper function for acquiring the cheatsheet and ending the game."""
    print()
    print("Sort CHEATSHEET into the correct album pile: "
          "[1: Fearless, 2: 1989, 3: Rep., 4: Folklore, 5: Lover, 6: Red]\n")
    get_cheat_sheet = input("Wait! Is that an unusual spotting! "
                            "[acquire] the item before it gets lost again ")
    while get_cheat_sheet != 'acquire':
        get_cheat_sheet = input("Try again! [acquire] it before it gets lost in the midst of MLC.")
    # Simulate finding the cheat sheet after successful sorting
    acquire_all_except(local_world, local_player)
    player.tbucks += 500
    print("\n-- You have been gifted 500 Tbucks for obtaining the required item -- \n")
    print("--------------------------------------------")
    inp = input()
    if inp == 'inventory':
        player.show_inventory()
        print("You have cleared all the puzzle in the game!")
    else:
        print("You have cleared all the puzzle in the game!")
    flip_blackboard()


def helper_sort() -> Optional:
    """A helper function to simulate sorting Taylor Swift songs into the correct album piles."""
    albums_songs = {
        'Lover': 'Lover',
        'All Too Well (From The Vault)': 'Red (Taylor’s Version)',
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
            if mistakes == 3:
                return False  # Too many mistakes, game over

            print(f"\nSort the song '{song}' into the correct album pile: "
                  "[1: Fearless, 2: 1989, 3: Rep., 4: Folklore, 5: Lover, 6: Red]")
            inp = input("Pile number: ")
            if not inp.isdigit():
                print("Please enter a valid number.")
            elif int(inp) < 1 or int(inp) > 6:
                print("Invalid album choice. Please try again.")
            elif albums[correct_album] == int(inp):
                print(f"'{song}' sorted correctly into '{correct_album}'.")
                break
            else:
                print("Incorrect album. Please try again.")
                mistakes += 1
    return True


def flip_blackboard() -> Optional:
    """
    A function to conclude the game by checking player's inventory, Tbucks, and offering a final message.
    """
    # Prompt for inventory check
    print("\nBefore you head to the exam center, "
          "let's make sure you have everything you need (and all the other stuff you found)!")
    player.show_inventory()
    wrapper()

    # Flip the blackboard
    print("\nAs you prepare to leave, you notice something written on the blackboard.")
    flip = input("Flip the blackboard to read the message? (yes/no): ").strip().lower()

    if flip == "yes":
        player.step_counts += 1
        print("\n==========================================================================================")
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


def handle_librarian_interaction(local_command: str, local_librarian: Librarian) -> Optional:
    """ handle any interaction with the librarian. """
    if local_command.startswith('loot'):

        # Example trade logic
        print("Trade begins! Use commands like... \n"
              "[my inventory] : to check your Inventory \n"
              "[trade] : trade unused item for T-bucks \n"
              "[bargain for more] : to ask nicely for MORE T-bucks \n"
              "[stop trade] : to Exit and leave librarian alone \n "
              "WARNING: after [stop] you cannot loot this poor soul again")
    while True:
        inp = input(">> ").strip().lower()
        if len(inp.split()) >= 2:
            do, item = inp.split(' ', 1)
            if do == 'trade':
                player.step_counts += 1
                local_librarian.trade_for_bucks(player, item)
            elif do == 'my' and item == 'inventory':
                player.show_inventory()
            elif do.startswith('bargain'):
                player.step_counts += 1
                local_librarian.bargain(player)
                print("--warning: You are using up your available moves by bargaining!")
            elif do.startswith('stop'):
                player.step_counts += 1
                local_librarian.interacted = True
                print("Librarian: Phew! Thank you for leaving me alone")
                time.sleep(0.02)
                print("Type 'look' to keep exploring the location")
                return False
        else:
            if inp in actions:
                actions[inp]()
            else:
                print(f"{inp} what? Be rigorous.")


def check_move_status(move_status: str, new_x: int, new_y: int, local_world: World, local_librarian: Librarian) -> None:
    """Handle printing instructions based on the current move status and player's current location."""
    if move_status == "valid":
        player.step_counts += 1
        location_index = local_world.map[new_x][new_y]
        new_location = local_world.locations[location_index]
        if new_location.unlocked:
            local_librarian.interacted = False
            player.x, player.y = new_x, new_y
            lib_index = local_world.map[player.x][player.y]
            librarian_present = lib_index in local_librarian.spawn_locations and not local_librarian.interacted
            if local_world.locations[location_index + 1].unlocked and librarian_present:
                print(new_location.description)
            elif local_world.locations[location_index + 1].unlocked and not librarian_present:
                print(new_location.description)
                print("But there is nothing else to look at here. It's time to move on.")
            elif not local_world.locations[location_index + 1].unlocked:
                print(new_location.long_description)
        else:
            print("This location is locked. You can't enter yet.")
    else:
        print("You can't go that way or it's out of bounds.")


def look_action(local_world: World) -> bool:
    """Handle look command based on the location of the player."""
    curr_location = local_world.get_location(player.x, player.y)
    if curr_location and curr_location.unlocked:
        print(curr_location.look())
    else:
        print("There's nothing to look at here.")
    return True


def handle_command(local_command: str, local_world: World, local_player: Player,
                   local_librarian: Librarian, local_traded: bool, local_used: bool) -> Optional:
    """Handle the move commands between each location. Check move status and move player accordingly.
    Call each location's handle function when current_location_index is updated. Handle all other commands."""
    global max_count
    current_location_index = local_world.map[local_player.x][local_player.y]

    sub_actions = {
        'quit': lambda: False,  # Signal to exit the game loop
        'interaction': lambda: print(
            f"You have {max_count - player.step_counts + 1} interactions left before the exam starts!"),
        'help': lambda: print(f"Available commands: {local_world.get_location(player.x, player.y).valid_commands}"),
        'score': lambda: print(
            f"You currently have {player.tbucks} Tbucks. Trade with the librarian for to obtain more."),
        'hint': lambda: print("It's time to go on.") if
        local_world.locations[current_location_index + 1].unlocked else print(
            local_world.get_location(local_player.x, local_player.y).hint),
        'look': lambda: look_action(local_world),
    }

    command_parts = local_command.split()

    if len(command_parts) < 2 and 'go' in command_parts:
        print("Please specify a direction to go. Example: 'go north'")
        return True
    if local_command.startswith('go'):
        _, direction = local_command.split()
        if direction.lower() not in ['north', 'south', 'east', 'west']:
            print("Please specify a direction to go. Example: 'go north'")
        else:
            move_status, new_x, new_y = local_player.move(direction, local_world.map)
            check_move_status(move_status, new_x, new_y, local_world, local_librarian)
            current_location_index = local_world.map[local_player.x][local_player.y]

    elif local_command in sub_actions:
        sub_actions[local_command]()

    lib_index = local_world.map[player.x][player.y]
    librarian_present = lib_index in local_librarian.spawn_locations and not local_librarian.interacted
    if librarian_present:
        print("You're in a territory with a librarian that can trade with you. Type [loot] to begin trading.")
        if local_command.startswith('loot'):
            handle_librarian_interaction(local_command, local_librarian)
            return True

    if local_player.step_counts > max_count:
        print("Game Over: you ran out of moves. The exam started. You didn't make it there on time.")
        return False
    elif local_player.step_counts + 1 > max_count - 10:
        print(f"[WARNING] Be wise! {max_count - local_player.step_counts + 1} moves until the exam starts")

    location_handlers = {
        0: lambda: handle_location0(local_world, local_player),
        1: lambda: handle_location1(local_world, local_player, local_traded),
        2: lambda: handle_location2(local_command, local_world),
        3: lambda: handle_location3(local_command, local_world, local_player, local_used),
        4: lambda: handle_location4(local_command, local_world, local_player),
        5: lambda: handle_location5(local_world, local_player),
        6: lambda: handle_location6(local_world, local_player),
    }
    if current_location_index in location_handlers:
        return location_handlers[current_location_index]()

    return None


def acquire_all_except(local_world: World, local_player: Player, it: str = None) -> None:
    """add all items in the location to the player's inventory except one item (optional)."""
    for item in local_world.get_location(local_player.x, local_player.y).items:
        if it is not None:
            if not item.name.lower() == it:
                local_player.acquire(item)
        else:
            local_player.acquire(item)


def acquire_only(local_world: World, local_player: Player, it: str = None) -> None:
    """add only one specified item in the location to the player's inventory."""
    for item in local_world.get_location(player.x, player.y).items:
        if it is not None:
            if item.name.lower() == it:
                local_player.acquire(item)


def blank_lines(user_input: str, length: int) -> None:
    """Print blank line prompt for puzzle"""
    display = ['_' for _ in range(length)]
    for i, char in enumerate(user_input):
        if i < len(display):
            display[i] = char
            print("\r" + " ".join(display), end="")
            time.sleep(0.5)


def print_progress_bar(word: str, duration: float = 0.05, width: int = 30) -> None:
    """Prints a simple progress bar in the console over a given duration of time."""
    for i in range(width + 1):
        percent = (i / width) * 100
        barr = '#' * i + '-' * (width - i)
        print(f"\r{word}: [{barr}] {percent: .2f}%", end="")
        time.sleep(duration / width)
    print()


def print_rules() -> None:
    """ Print the game's starting screen."""
    print("-----------------")
    print("Game Objective: It's the morning of a big test, and you realize you've lost your three essential items: \n"
          "1. Your Lucky pen\n"
          "2. Cheat Sheet\n"
          "3. TCard \n"
          "Your mission is to navigate the world and 'acquire' these items in your inventory before the test begins.")
    # print("-----------------")
    # inp = input("Press [enter] to continue ")
    print("-----------------")
    print("(*) General Commands:\n"
          "[quit]: Exit the game \n"
          "[go [direction]]: Move player in the specified direction \n"
          "[inventory]: Show player's inventory \n"
          "[look]: Print the brief description for player's current location \n"
          "[hint]: Provide game hints for each location \n"
          "[help]: Show all available commands in player's current location \n"
          "[interaction]: Show the number of interactions left before the exam starts \n"
          "[item]: Show all obtainable items in player's current location \n"
          "[score]: Show player's current amount of Tbucks (score) \n"
          "Notes: Some commands are not available while solving specific puzzles.")
    print("-----------------")
    # inp = input("Press [enter] to continue ")
    # print("-----------------")
    print("(*) Interaction Limit: You have exactly 42 interactions.\n"
          "Each valid command you enter except the General Commands (see above), some event interactions, \n"
          "and input to the Final Challenge counts as one interaction. Choose wisely to avoid a premature game over! \n"
          "You can type 'help' to see the valid commands in each location.")
    print("-----------------")
    # inp = input("Press [enter] to continue ")
    # print("-----------------")
    print(
        "(*) Scoring: Throughout your quest, you'll earn Tbucks by completing side quests. Your prowess in acquiring \n"
        "Tbucks will determine your final rank: GOLD, SILVER, or BRONZE. \n"
        "To earn Tbucks, you must engage with the RANDOMLY SPAWNING LIBRARIANS, \n"
        "either by trading items or by bargaining for a extra Tbucks.")
    # print("-----------------")
    # inp = input("Press [enter] to continue ")
    print("-----------------")
    print("(*) Final Challenge: In the last room, you are tasked with sorting critical information correctly. \n"
          "CAREFUL: You only get six attempts to place everything in its right place. Fail, and it's game over.")
    print("-------------")
    # inp = input("Press [enter] to start the game")
    # print("-----------------")


def determine_rank(dollars: int, moves: int, max_dollars: int, max_moves: int) -> str:
    """Calculate final ranking based on the amount of dollars and max_moves"""
    dollars_percentage = dollars / max_dollars
    moves_percentage = moves / max_moves

    # Define thresholds for each rank
    gold_threshold = 0.8
    silver_threshold = 0.6

    score = 0
    if dollars_percentage >= gold_threshold:
        score += 80
    elif dollars_percentage >= silver_threshold:
        score += 60
    else:
        score += 0

    if moves_percentage >= gold_threshold:
        score += 0
    elif moves_percentage >= silver_threshold:
        score += 60
    else:
        score += 80

    if score >= gold_threshold * 160:
        return 'Gold'
    elif score >= silver_threshold * 160:
        return 'Silver'
    else:
        return 'Bronze'


def wrapper() -> None:
    """Print player's game summary and suggestions."""
    tbucks = player.tbucks
    all_items = [it for loc in world.locations for it in world.locations[loc].items]
    all_worth = sum([it.worth for it in all_items if it.worth > 0])
    all_worth += 1500
    missed = [it for it in player.inventory if it.name.lower() not in ['tcard', 'cheatsheet', 'lucky pen']]
    missed_worth = sum([it.worth for it in missed if it.worth > 0])
    rank = determine_rank(tbucks, player.step_counts, all_worth, 42)
    print()
    time.sleep(1)
    if all_worth > tbucks:
        print("You missed out on:")
        print(f"- {missed_worth} Tbucks from not trading the following items with the librarian: ")
        for item in missed:
            print(f"- {item.name} ({item.worth} Tbucks)")
    time.sleep(1)
    print()
    print("Achievements:")
    time.sleep(1)
    print(f"- You finished the game with {player.step_counts} interactions.")
    time.sleep(1)
    print(f"- You have earned {tbucks} Tbucks in total.")
    time.sleep(1)
    print(f"- Based on your Tbucks and interaction count, you've earned a {rank} ranking!")


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['hashlib']
    })
    with open('map.txt') as map_file, open('locations.txt') as location_file, open('items.txt') as item_file:
        world = World(map_file, location_file, item_file)
    player = Player(0, 0)
    librarian = Librarian(0, 0, "Librarian")
    # Seed for Demo Purposes
    librarian.spawn_seed(10)
    print(librarian.spawn_locations)
    # Set up
    current_painting_index = 0
    traded = False
    used = False
    max_count = 42

    actions = {
        "inventory": player.show_inventory,
        "interaction": lambda: print(
            f"You have {max_count - player.step_counts + 1} interactions left before the exam starts!"),
        "hint": lambda: print(world.get_location(player.x, player.y).hint),
        "help": lambda: print(f"Available commands: {world.get_location(player.x, player.y).valid_commands}"),
        "item": lambda: print(
            f"Available items here: {[it.name for it in world.get_location(player.x, player.y).items]}"),
        "score": lambda: print(f"You currently have {player.tbucks} Tbucks. Trade with the librarian to obtain more."),
        "go": lambda: print("Why would you want to go away? There is something interesting here."),
        "quit": lambda: False
    }

    print("Welcome to Text Adventure Game!")
    print("""

        █░░░█ █▀▀ █░░ █▀▀ █▀▀█ █▀▄▀█ █▀▀ 　 ▀▀█▀▀ █▀▀█ 　 █░░█ █▀▀█ █▀▀ ▀▀█▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀
        █▄█▄█ █▀▀ █░░ █░░ █░░█ █░▀░█ █▀▀ 　 ░░█░░ █░░█ 　 █░░█ █░░█ █▀▀ ░░█░░ █▀▀ █▄▄█ █▄▄▀ ▀▀█
        ░▀░▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░░░▀ ▀▀▀ 　 ░░▀░░ ▀▀▀▀ 　 ░▀▀▀ ▀▀▀▀ ▀░░ ░░▀░░ ▀▀▀ ▀░░▀ ▀░▀▀ ▀▀▀

    """)
    start_choice = input("Type [Read Rules]: ")
    while start_choice.lower() != 'read rules':
        start_choice = input("Try Again! Type [Read Rules]: ")
    print()
    print_rules()

    time.sleep(1)
    s_short = 0.25
    time.sleep(s_short)
    world.locations[0].unlock()
    player.set_location(1, 1)
    print(world.get_location(player.x, player.y).long_description)
    print("Try type [start] to embark on your adventure: ")

    continue_game = True
    while continue_game:
        current_location = world.get_location(player.x, player.y)
        command = input(">> ").strip().lower()
        continue_game = handle_command(command, world, player, librarian, traded, used)
        if command == 'item':
            print(f"Available items here: {[item.name for item in world.get_location(player.x, player.y).items]}")
        elif command == 'inventory':
            player.show_inventory()
