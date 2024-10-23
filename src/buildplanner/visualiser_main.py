import argparse
import random
from turtle import mainloop, Screen

from buildplanner.parser_util import MOVE_STRATEGIES, ALIGNMENT_STRATEGIES, BONDS
from buildplanner.render import Renderer
from buildplanner.robot import (
    Robot,
    MoveStrategy,
)
from buildplanner.wall import Bond, create_wall

WALL_LENGTH = 2300
WALL_HEIGHT = 2000
ROBOT_BUILD_ENVELOPE_LENGTH = 800
ROBOT_BUILD_ENVELOPE_HEIGHT = 1300


def main(bond: Bond, move_strategy: MoveStrategy):
    wall = create_wall(WALL_LENGTH, WALL_HEIGHT, bond)
    robot = Robot(
        ROBOT_BUILD_ENVELOPE_LENGTH,
        ROBOT_BUILD_ENVELOPE_HEIGHT,
        move_strategy,
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


def parse_args() -> (Bond, MoveStrategy):
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bond", choices=BONDS.keys(), default="stretcher")
    parser.add_argument(
        "-m",
        "--move-strategy",
        choices=MOVE_STRATEGIES.keys(),
        default="outside_in",
    )
    parser.add_argument(
        "-a",
        "--alignment-strategy",
        choices=ALIGNMENT_STRATEGIES.keys(),
    )

    args = parser.parse_args()
    default_align = "right" if args.bond == "flemish" else "center"
    return (
        BONDS[args.bond](),
        MOVE_STRATEGIES[args.move_strategy](
            ALIGNMENT_STRATEGIES[args.alignment_strategy or default_align]()
        ),
    )


if __name__ == "__main__":
    main(*parse_args())
