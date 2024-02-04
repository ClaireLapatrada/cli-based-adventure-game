import sys
import subprocess


print('help')
p = subprocess.getoutput("{} ./adventure2.py < solution.txt".format(sys.executable))
print(p)
