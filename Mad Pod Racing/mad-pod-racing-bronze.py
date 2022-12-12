import sys
import math

# Guidelines
checkpoint_radius = 600
slowingdown_dist = 1500
boost_dist = 5000
boost_angle = 1
thrust_max_angle = 20
thrust_max = 100
thrust_min = 0
booster = 0

# Game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    (
        x,
        y,
        next_checkpoint_x,
        next_checkpoint_y,
        next_checkpoint_dist,
        next_checkpoint_angle,
    ) = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    x = next_checkpoint_x
    y = next_checkpoint_y
    thrust = thrust_max

    # Hit the opponent right from the start
    if booster == 0:
        x, y = opponent_x, opponent_y
        thrust = "BOOST"
        print(str(x) + " " + str(y) + " " + str(thrust))
        booster += 1
    else:
        if next_checkpoint_angle > 90 or next_checkpoint_angle < -90:
            thrust = 0

        elif next_checkpoint_dist <= 500:
            thrust = 0
        else:
            thrust = 100

        print(str(x) + " " + str(y) + " " + str(thrust))

    # next checkpoint is behind
    # if abs(next_checkpoint_angle) > 90:
    #    thrust = thrust_min

    # next checkpoint is on the side
    # elif thrust_max_angle <= abs(next_checkpoint_angle) <= 90:
    # if the pod is misaligned, the pod slows down to rotate
    #    slowdown_to_rotate = 1 - abs(next_checkpoint_angle / 90)
    #    thrust = int(thrust_max * slowdown_to_rotate)

    # checkpoint is straight ahead, PUNCH IT!
    # elif abs(next_checkpoint_angle) <= thrust_max_angle :
    #    if abs(next_checkpoint_angle) <= boost_angle and next_checkpoint_dist > boost_dist:
    #        thrust = thrust_max
    # else :
    #    thrust = thrust_max

    # if next_checkpoint_angle > 90 or next_checkpoint_angle < -90:
    #    thrust = 0
    # elif next_checkpoint_dist <= 600 : thrust = 20
    # else : thrust = 100

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
