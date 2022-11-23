import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
list_pi = []

for i in range(n):
    pi = int(input())
    list_pi.append(pi)

list_pi.sort()
arr_pi = np.array(list_pi)
difference = abs(np.ediff1d(arr_pi))
result = np.min(difference)   

print(result)