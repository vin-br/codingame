import sys
import math

# The while loop represents the game.
# Each iteration represents a turn of the game
# where you are given inputs (the heights of the mountains)
# and where you have to print an output (the index of the mountain to fire on)
# The inputs you are given are automatically updated according to your last actions.


# game loop
while True:
    highest_mountain = 0
    highest_mountain_index = 1
    for i in range(8):
        mountain_height = int(input())  # represents the height of one mountain.
        if mountain_height > highest_mountain :
            highest_mountain = mountain_height
            highest_mountain_index = i

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # The index of the mountain to fire on.
    print(highest_mountain_index)