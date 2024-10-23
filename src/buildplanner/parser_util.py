from buildplanner.robot import (
    LeftToRightMoveStrategy,
    OutsideInMoveStrategy,
    SnakeMoveStrategy,
    DynamicSnakeMoveStrategy,
    LeftAlignmentStrategy,
    RightAlignmentStrategy,
    CenterAlignmentStrategy,
    RandomAlignmentStrategy,
)
from buildplanner.wall import StretcherBond, CrossBond, FlemishBond, WildBond

BONDS = {
    "stretcher": StretcherBond,
    "cross": CrossBond,
    "flemish": FlemishBond,
    "wild": WildBond,
}
MOVE_STRATEGIES = {
    "left_to_right": LeftToRightMoveStrategy,
    "outside_in": OutsideInMoveStrategy,
    "snake": SnakeMoveStrategy,
    "dynamic_snake": DynamicSnakeMoveStrategy,
}
ALIGNMENT_STRATEGIES = {
    "left": LeftAlignmentStrategy,
    "right": RightAlignmentStrategy,
    "center": CenterAlignmentStrategy,
    "random": RandomAlignmentStrategy,
}


def int_greater_than_0(val: str) -> int:
    val = int(val)
    if val < 1:
        raise ValueError("Must be an int greater than 0")
    return val
