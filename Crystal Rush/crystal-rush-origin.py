import sys
import math

# Deliver more ore to hq (left side of the map) than your opponent. Use radars to find ore but beware of traps!

# height: size of the map
width, height = [int(i) for i in input().split()]

# game loop
while True:
    # my_score: Amount of ore delivered
    my_score, opponent_score = [int(i) for i in input().split()]
    for i in range(height):
        inputs = input().split()
        for j in range(width):
            # ore: amount of ore or "?" if unknown
            # hole: 1 if cell has a hole
            ore = inputs[2 * j]
            hole = int(inputs[2 * j + 1])
    # entity_count: number of entities visible to you
    # radar_cooldown: turns left until a new radar can be requested
    # trap_cooldown: turns left until a new trap can be requested
    entity_count, radar_cooldown, trap_cooldown = [int(i) for i in input().split()]
    for i in range(entity_count):
        # entity_id: unique id of the entity
        # entity_type: 0 for your robot, 1 for other robot, 2 for radar, 3 for trap
        # y: position of the entity
        # item: if this entity is a robot, the item it is carrying (-1 for NONE, 2 for RADAR, 3 for TRAP, 4 for ORE)
        entity_id, entity_type, x, y, item = [int(j) for j in input().split()]
    for i in range(5):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # WAIT|MOVE x y|DIG x y|REQUEST item
        print("WAIT")
