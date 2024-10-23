import itertools

from buildplanner.robot import (
    LeftAlignmentStrategy,
    RightAlignmentStrategy,
    CenterAlignmentStrategy,
    RandomAlignmentStrategy,
    LeftToRightMoveStrategy,
    OutsideInMoveStrategy,
    SnakeMoveStrategy,
    Robot,
    DynamicSnakeMoveStrategy,
)
from buildplanner.wall import create_wall, StretcherBond

WALL_LENGTH = 2300
WALL_HEIGHT = 2000
ROBOT_BUILD_ENVELOPE_LENGTH = 800
ROBOT_BUILD_ENVELOPE_HEIGHT = 1300

BOND = StretcherBond()


def try_all_move_strategies():
    alignment_strategies = [
        LeftAlignmentStrategy,
        RightAlignmentStrategy,
        CenterAlignmentStrategy,
        RandomAlignmentStrategy,
    ]
    move_strategies = [
        LeftToRightMoveStrategy,
        OutsideInMoveStrategy,
        SnakeMoveStrategy,
        DynamicSnakeMoveStrategy,
    ]

    for alignment_strategy, move_strategy in itertools.product(
        alignment_strategies, move_strategies
    ):
        print("Trying ", alignment_strategy.__name__, move_strategy.__name__)
        wall = create_wall(WALL_LENGTH, WALL_HEIGHT, BOND)
        robot = Robot(
            ROBOT_BUILD_ENVELOPE_LENGTH,
            ROBOT_BUILD_ENVELOPE_HEIGHT,
            move_strategy(alignment_strategy()),
        )
        while True:
            if robot.lay_brick(wall) is None:
                if not robot.move(wall):
                    break
        print("Total number of strides: ", robot.move_count + 1)


if __name__ == "__main__":
    try_all_move_strategies()
