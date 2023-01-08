import sys
import math
import random

# height: size of the map
width, height = [int(i) for i in input().split()]

NONE = -1
ROBOT_ALLY = 0
ROBOT_ENEMY = 1
HOLE = 1
RADAR = 2
TRAP = 3
AMADEUSIUM = 4


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, pos):
        return abs(self.x - pos.x) + abs(self.y - pos.y)


class Entity(Pos):
    def __init__(self, x, y, an_id):
        super().__init__(x, y)
        self.id = an_id


class Robot(Entity):
    def __init__(self, x, y, an_id, item):
        super().__init__(x, y, an_id)
        self.item = item
        self.destination = None

    def is_dead(self):
        return self.x == -1 and self.y == -1

    def move(self, x, y, message=""):
        if x > self.x:
            x -= 1
        elif y > self.y:
            y -= 1
        elif y < self.y:
            y += 1

        print(f"MOVE {x} {y} {message}")

    def wait(self, message=""):
        print(f"{self.id}: Gonna wait saying '{message}'", file=sys.stderr)
        print(f"WAIT {message}")

    def dig(self, cell, message=""):
        print(f"DIG {cell.x} {cell.y} {message}")

    def request(self, requested_item, message=""):
        # self.destination = None
        if requested_item == RADAR:
            print(f"REQUEST RADAR {message}")
        elif requested_item == TRAP:
            print(f"REQUEST TRAP {message}")
        else:
            raise Exception(f"Unknown item {requested_item}")

    def move_at_random(self):
        randx = random.randint(0, 30)
        randy = random.randint(0, 15)
        self.move(randx, randy, "Bip bip!")

    def run(self):
        if self.item == AMADEUSIUM:
            self.move(0, self.y)
            return

        if self.item == RADAR or self.item == TRAP:
            self.dig(self.destination)
            return

        # Radar request conditions
        if (
            game.radar_requested == False
            and self.x == 0
            and self.item == -1
            and len(game.radar_spots) > 0
            and game.radar_cooldown == 0
        ):
            self.destination = game.radar_spots.pop(0)
            self.request(RADAR, "Call me Radar")
            game.radar_requested = True
            game.nb_radars_requested += 1
            return

        # if game.radar_cooldown == 0 :
        #     game.radar_requested = False

        # Trap request conditions
        # if (
        #     game.trap_requested == False and
        #     self.x == 0 and
        #     self.item == -1 and
        #     len(game.trap_spots) > 0 and
        #     game.trap_cooldown == 0
        # ):
        #     self.destination = game.trap_spots.pop(0)
        #     self.request(TRAP, "Kaboom Boom")
        #     game.trap_requested = True
        #     game.nb_traps_requested += 1
        #     return

        # Robots going to the closest spot available
        sorted_cells = sorted(game.grid.cells, key=lambda c: self.distance(c))
        for cell in sorted_cells:
            if cell.amadeusium > 0:
                self.dig(cell, "Cha-Ching!")
                return

        if game.radar_cooldown == 0 and game.nb_radars_requested <= 6:
            self.move(0, self.y)
            return

        # if game.trap_cooldown == 0 and game.nb_traps_requested <= 6:
        #         self.move(0, self.y)
        #         return

        if cpturn % 3 == 0:
            self.dig(self)
            return

        self.move_at_random()


class Cell(Pos):
    def __init__(self, x, y, amadeusium, hole):
        super().__init__(x, y)
        self.amadeusium = amadeusium
        self.hole = hole
        self.radar = False

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def has_hole(self):
        return self.hole == HOLE

    def update(self, amadeusium, hole):

        if self.amadeusium == 0 and amadeusium <= 0:
            amadeusium = 0

        self.amadeusium = amadeusium
        self.hole = hole

    @property
    def has_radar(self):
        return self.radar

    def put_radar(self):
        self.radar = True

    def remove_radar(self):
        self.radar = False


class Grid:
    def __init__(self):
        self.cells = []
        for y in range(height):
            for x in range(width):
                self.cells.append(Cell(x, y, -1, 0))

    def get_cell(self, x, y) -> Cell:
        if width > x >= 0 and height > y >= 0:
            return self.cells[x + width * y]
        raise Exception("Can't get a cell that's out of the grid!")


class Game:
    def __init__(self):
        self.grid = Grid()
        self.total_known_amadeusium = 0
        self.my_score = 0
        self.enemy_score = 0
        self.radar_cooldown = 0
        self.trap_cooldown = 0
        self.radars = []
        self.radar_requested = False
        self.nb_radars_requested = 0
        self.radar_spots = [
            self.grid.get_cell(5, 7),
            self.grid.get_cell(5, 3),
            self.grid.get_cell(5, 11),
            self.grid.get_cell(12, 7),
            self.grid.get_cell(12, 3),
            self.grid.get_cell(12, 11),
            self.grid.get_cell(19, 7),
            self.grid.get_cell(19, 3),
            self.grid.get_cell(19, 11),
            self.grid.get_cell(26, 7),
            self.grid.get_cell(26, 3),
            self.grid.get_cell(26, 11),
        ]
        # self.traps = []
        # self.trap_requested = False
        # self.nb_traps_requested = 0
        # self.trap_spots = [
        #     self.grid.get_cell(9, 9),
        #     self.grid.get_cell(8, 13),
        #     self.grid.get_cell(16, 3),
        #     self.grid.get_cell(17, 9)
        # ]
        self.my_robots = []
        self.enemy_robots = []

    def reset(self):
        self.radars = []
        self.traps = []
        self.radar_requested = False
        self.trap_requested = False

    def get_my_robot_by_id(self, an_id) -> Robot:
        for robot in self.my_robots:
            if robot.id == an_id:
                return robot
        raise Exception(f"Unknown ally robot with ID {an_id}!")

    def get_enemy_robot_by_id(self, an_id):
        for robot in self.enemy_robots:
            if robot.id == an_id:
                return robot
        raise Exception(f"Unknown ennemy robot with ID {an_id}!")

    def update_my_robot(self, x, y, an_id, item):
        robot = self.get_my_robot_by_id(an_id)
        robot.x = x
        robot.y = y
        robot.item = item

    def update_enemy_robot(self, x, y, an_id, item):
        robot = self.get_enemy_robot_by_id(an_id)
        robot.x = x
        robot.y = y
        robot.item = item


game = Game()

# Turn counter
cpturn = 1
# game loop
while True:
    # my_score: Players score
    game.my_score, game.enemy_score = [int(i) for i in input().split()]
    unknown_cells_cpt = 0
    total_known_amadeusium = 0
    for i in range(height):
        # str_cells = ""
        inputs = input().split()
        for j in range(width):
            # the_amadeusium: amount of amadeusium or "?" if unknown
            # the_hole: 1 if cell has a hole

            cur_cell = game.grid.get_cell(j, i)
            the_amadeusium = inputs[2 * j]
            if the_amadeusium == "?":
                the_amadeusium = -1
            else:
                the_amadeusium = int(the_amadeusium)

            # str_cells += f"[{str(the_amadeusium).center(4)}]"
            the_hole = int(inputs[2 * j + 1])
            cur_cell.update(the_amadeusium, the_hole)

        # print(f"{str_cells}", file=sys.stderr)

    game.total_known_amadeusium = total_known_amadeusium

    # entity_count: number of entities visible to you
    # radar_cooldown: turns left until a new radar can be requested
    # trap_cooldown: turns left until a new trap can be requested
    entity_count, game.radar_cooldown, game.trap_cooldown = [int(i) for i in input().split()]

    game.reset()
    cpt_roles = 0

    for i in range(entity_count):
        # the_id: unique id of the entity
        # a_type: 0 for your robot, 1 for other robot, 2 for radar, 3 for trap
        # y: position of the entity
        # item: if this entity is a robot,
        # the item it is carrying (-1 for NONE, 2 for RADAR, 3 for TRAP, 4 for AMADEUSIUM)
        the_id, a_type, the_x, the_y, the_item = [int(j) for j in input().split()]

        if a_type == ROBOT_ALLY:
            if cpturn == 1:
                game.my_robots.append(Robot(the_x, the_y, the_id, the_item))
            else:
                game.update_my_robot(the_x, the_y, the_id, the_item)
        elif a_type == ROBOT_ENEMY:
            if cpturn == 1:
                game.enemy_robots.append(Robot(the_x, the_y, the_id, the_item))
            else:
                game.update_enemy_robot(the_x, the_y, the_id, the_item)

        elif a_type == TRAP:
            print(f"Trap found at [{the_x}, {the_y}]!!!", file=sys.stderr)
            game.traps.append(Entity(the_x, the_y, the_id))
        elif a_type == RADAR:
            game.radars.append(Entity(the_x, the_y, the_id))

    for i in range(len(game.my_robots)):
        game.my_robots[i].run()

    cpturn += 1
