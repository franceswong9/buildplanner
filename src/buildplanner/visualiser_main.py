import random
from turtle import mainloop, Screen

from buildplanner.render import Renderer
from buildplanner.robot import Robot, OutsideInMoveStrategy, CenterAlignmentStrategy
from buildplanner.wall import create_wall, StretcherBond

WALL_LENGTH = 2300
WALL_HEIGHT = 2000
ROBOT_BUILD_ENVELOPE_LENGTH = 800
ROBOT_BUILD_ENVELOPE_HEIGHT = 1300

## most efficient for the stretcher and cross bond wall
BOND = StretcherBond()
# BOND = CrossBond()
ALIGNMENT_STRATEGY = CenterAlignmentStrategy()
MOVE_STRATEGY = OutsideInMoveStrategy(ALIGNMENT_STRATEGY)

## most efficient for the flemish bond wall
# BOND = FlemishBond()
# ALIGNMENT_STRATEGY = RightAlignmentStrategy()
# MOVE_STRATEGY = OutsideInMoveStrategy(ALIGNMENT_STRATEGY)


def main():
    wall = create_wall(WALL_LENGTH, WALL_HEIGHT, BOND)
    robot = Robot(
        ROBOT_BUILD_ENVELOPE_LENGTH,
        ROBOT_BUILD_ENVELOPE_HEIGHT,
        MOVE_STRATEGY,
    )

    screen = Screen()
    screen.tracer(False)
    screen.setworldcoordinates(0, 0, WALL_LENGTH, WALL_HEIGHT)

    renderer = Renderer()
    renderer.render_wall(wall)

    colours = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(100)]

    def render_brick():
        brick = robot.lay_brick(wall)
        if brick is None:
            if robot.move(wall):
                brick = robot.lay_brick(wall)
        if brick is not None:
            stride = robot.move_count + 1
            renderer.render_brick(brick, colours[stride], stride)

    screen.onkey(render_brick, "Return")
    screen.listen()

    mainloop()


if __name__ == "__main__":
    main()
