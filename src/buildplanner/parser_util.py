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
from buildplanner.wall import StretcherBond, CrossBond, FlemishBond

BONDS = {
    "stretcher": StretcherBond,
    "cross": CrossBond,
    "flemish": FlemishBond,
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
