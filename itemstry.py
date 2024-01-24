import time
from game_data2 import World, Item, Location, Player

if __name__ == "__main__":
    world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    player = Player(0, 0)

    s_short = 0.5
    print("Welcome to the Text Adventure Game!")
    print("Rules and Regulations")
    # press help
    time.sleep(s_short)
    print("You wake up in your room and see a squirrel outside your window.\nYou find out that your"
          " T card, Lucky Pen, and Cheat Sheet is missing! Your CSC111 Test is today and you start to panic\n"
          "Catch me in you can it says. Desperate, you run in its direction. ")
    time.sleep(s_short)
    print("you enter an empty green room")
    player.set_location(0, 1)
    location = world.get_location(player.x, player.y)
    print(location.long_description)
    Vending = Item("Vending Machine", {})
    command = input(">> ").strip().lower()

    vending_machine_pass = False
    while vending_machine_pass == False:
        if command.startswith('look'):
            print(location.look())
        elif command.startswith('press'):
            Vending.press()
        else:
            print('command not found')



