""" Run through the game with two solutions (solution.txt and gameover.txt)."""
import sys
import subprocess

solution = subprocess.getoutput("{} ./adventure.py < solution.txt".format(sys.executable))
# gameover = subprocess.getoutput("{} ./adventure.py < game_over.txt".format(sys.executable))
print(solution)
print("----")
# print(gameover)
