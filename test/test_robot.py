from buildplanner.robot import (
    Robot,
    LeftToRightMoveStrategy,
    CenterAlignmentStrategy,
    LeftAlignmentStrategy,
    RightAlignmentStrategy,
    RandomAlignmentStrategy,
    OutsideInMoveStrategy,
    SnakeMoveStrategy,
    DynamicSnakeMoveStrategy,
)
from buildplanner.util import Rectangle, Point
from buildplanner.wall import (
    create_wall,
    Brick,
    BED_JOINT_THICKNESS,
    COURSE_HEIGHT,
    StretcherBond,
)


def test_left_alignment_strategy():
    alignment_strategy = LeftAlignmentStrategy()
    brick = Brick(Rectangle(Point(14, BED_JOINT_THICKNESS), 2, 10))
    robot = Robot(10, 10, LeftToRightMoveStrategy(alignment_strategy))
    wall = create_wall(30, 30, StretcherBond())
    next_area = alignment_strategy.next_reachable_area(brick, robot, wall)
    assert next_area == Rectangle(Point(14, 0), 10, 10)


def test_right_alignment_strategy():
    alignment_strategy = RightAlignmentStrategy()
    brick = Brick(Rectangle(Point(14, 10 + BED_JOINT_THICKNESS), 2, 10))
    robot = Robot(10, 10, LeftToRightMoveStrategy(alignment_strategy))
    wall = create_wall(30, 30, StretcherBond())
    next_area = alignment_strategy.next_reachable_area(brick, robot, wall)
    assert next_area == Rectangle(Point(6, 10), 10, 10)


def test_center_alignment_strategy():
    alignment_strategy = CenterAlignmentStrategy()
    brick = Brick(Rectangle(Point(14, BED_JOINT_THICKNESS), 2, 10))
    robot = Robot(10, 10, LeftToRightMoveStrategy(alignment_strategy))
    wall = create_wall(30, 30, StretcherBond())
    next_area = alignment_strategy.next_reachable_area(brick, robot, wall)
    assert next_area == Rectangle(Point(10, 0), 10, 10)


def test_random_alignment_strategy():
    alignment_strategy = RandomAlignmentStrategy()
    brick = Brick(Rectangle(Point(14, BED_JOINT_THICKNESS), 2, 10))
    robot = Robot(10, 10, LeftToRightMoveStrategy(alignment_strategy))
    wall = create_wall(30, 30, StretcherBond())
    next_area = alignment_strategy.next_reachable_area(brick, robot, wall)
    assert 6 <= next_area.bottom_left_corner.x <= 14


def test_alignment_strategy_keeps_reachable_area_in_wall_boundaries_when_too_far_left():
    alignment_strategy = RightAlignmentStrategy()
    brick = Brick.create_full_brick(Point(0, BED_JOINT_THICKNESS))
    robot = Robot(10, 10, LeftToRightMoveStrategy(alignment_strategy))
    wall = create_wall(20, 20, StretcherBond())
    next_area = alignment_strategy.next_reachable_area(brick, robot, wall)
    assert wall.box.bounds(next_area)


def test_alignment_strategy_keeps_reachable_area_in_wall_boundaries_when_too_far_right():
    alignment_strategy = LeftAlignmentStrategy()
    brick = Brick.create_full_brick(Point(19, BED_JOINT_THICKNESS))
    robot = Robot(10, 10, LeftToRightMoveStrategy(alignment_strategy))
    wall = create_wall(20, 20, StretcherBond())
    next_area = alignment_strategy.next_reachable_area(brick, robot, wall)
    assert wall.box.bounds(next_area)


def test_alignment_strategy_keeps_reachable_area_in_wall_boundaries_when_too_far_up():
    alignment_strategy = LeftAlignmentStrategy()
    brick = Brick.create_full_brick(Point(0, 19))
    robot = Robot(10, 10, LeftToRightMoveStrategy(alignment_strategy))
    wall = create_wall(20, 20, StretcherBond())
    next_area = alignment_strategy.next_reachable_area(brick, robot, wall)
    assert wall.box.bounds(next_area)


def test_move_strategy_returns_none_when_wall_is_complete():
    wall = create_wall(2300, 2000, StretcherBond())
    move_strategy = LeftToRightMoveStrategy(LeftAlignmentStrategy())
    robot = Robot(800, 1300, move_strategy)
    for course in wall.courses:
        for unit in course.units:
            unit.is_built = True
    assert move_strategy.next_move(robot, wall) is None


def test_left_to_right_move_strategy():
    wall = create_wall(2300, 2000, StretcherBond())
    move_strategy = LeftToRightMoveStrategy(LeftAlignmentStrategy())
    robot = Robot(800, 1300, move_strategy)
    for unit in wall.courses[0].units[:4]:
        unit.is_built = True
    assert move_strategy.next_move(robot, wall) == Rectangle(Point(440, 0), 800, 1300)


def test_outside_in_move_strategy():
    wall = create_wall(2300, 2000, StretcherBond())
    move_strategy = OutsideInMoveStrategy(LeftAlignmentStrategy())
    robot = Robot(800, 1300, move_strategy)
    assert move_strategy.next_move(robot, wall) == Rectangle(Point(1500, 0), 800, 1300)
    assert move_strategy.next_move(robot, wall) == Rectangle(Point(0, 0), 800, 1300)
    assert move_strategy.next_move(robot, wall) == Rectangle(Point(1500, 0), 800, 1300)


def test_snake_move_strategy():
    wall = create_wall(2300, 2000, StretcherBond())
    move_strategy = SnakeMoveStrategy(LeftAlignmentStrategy())
    robot = Robot(800, 1300, move_strategy)
    assert move_strategy.next_move(robot, wall) == Rectangle(Point(0, 0), 800, 1300)
    for unit in wall.courses[0].units:
        unit.is_built = True
    assert move_strategy.next_move(robot, wall) == Rectangle(
        Point(1500, COURSE_HEIGHT), 800, 1300
    )
    for unit in wall.courses[1].units:
        unit.is_built = True
    assert move_strategy.next_move(robot, wall) == Rectangle(
        Point(0, 2 * COURSE_HEIGHT), 800, 1300
    )


def test_dynamic_snake_move_strategy():
    wall = create_wall(2300, 2000, StretcherBond())
    move_strategy = DynamicSnakeMoveStrategy(LeftAlignmentStrategy())
    robot = Robot(800, 1300, move_strategy)
    wall.courses[0].units[0].is_built = True
    assert move_strategy.next_move(robot, wall) == Rectangle(Point(0, 0), 800, 1300)
    for unit in wall.courses[0].units:
        unit.is_built = True
    wall.courses[1].units[-1].is_built = True
    wall.courses[1].units[-2].is_built = True
    assert move_strategy.next_move(robot, wall) == Rectangle(
        Point(1500, COURSE_HEIGHT), 800, 1300
    )


def test_robot_move():
    wall = create_wall(2300, 2000, StretcherBond())
    robot = Robot(800, 1300, OutsideInMoveStrategy(CenterAlignmentStrategy()))
    assert robot.move(wall)
    assert robot.move_count == 1
    assert robot.reachable_area == Rectangle(Point(1500, 0), 800, 1300)


def test_robot_move_returns_false_when_wall_is_complete():
    wall = create_wall(2300, 2000, StretcherBond())
    robot = Robot(800, 1300, LeftToRightMoveStrategy(CenterAlignmentStrategy()))
    for course in wall.courses:
        for unit in course.units:
            unit.is_built = True
    assert not robot.move(wall)


def test_robot_lay_brick():
    wall = create_wall(2300, 2000, StretcherBond())
    robot = Robot(800, 1300, LeftToRightMoveStrategy(CenterAlignmentStrategy()))
    brick = robot.lay_brick(wall)
    assert brick.is_built
    assert brick.box.bottom_left_corner == Point(0, BED_JOINT_THICKNESS)


def test_robot_lay_brick_returns_none_when_area_is_complete():
    wall = create_wall(2300, 2000, StretcherBond())
    robot = Robot(800, 1300, LeftToRightMoveStrategy(CenterAlignmentStrategy()))
    for course in wall.courses:
        for unit in course.units:
            unit.is_built = True
    assert robot.lay_brick(wall) is None
