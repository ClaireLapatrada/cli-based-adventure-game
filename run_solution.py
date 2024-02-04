import sys
import subprocess


print('help')
p = subprocess.getoutput("{} ./adventure.py < solution.txt".format(sys.executable))
p2 = subprocess.getoutput("{} ./adventure.py < game_over.txt".format(sys.executable))
print(p)
print("----")
print(p2)
