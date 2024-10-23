from buildplanner.util import Point, Rectangle
from buildplanner.wall import (
    Brick,
    Course,
    Wall,
    create_wall,
    HeadJoint,
    HALF_BRICK_LENGTH,
    FULL_BRICK_LENGTH,
    HEAD_JOINT_THICKNESS,
    StretcherBond,
    CrossBond,
    QUARTER_BRICK_LENGTH,
    FlemishBond,
    THREE_QUARTER_BRICK_LENGTH,
)


def test_create_full_brick():
    brick = Brick.create_full_brick(Point(0, 0))
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == 210
    assert brick.box.height == 50
    assert not brick.is_built


def test_create_three_quarter_brick():
    brick = Brick.create_three_quarter_brick(Point(3, 4))
    assert brick.box.bottom_left_corner == Point(3, 4)
    assert brick.box.length == 155
    assert brick.box.height == 50
    assert not brick.is_built


def test_create_half_brick():
    brick = Brick.create_half_brick(Point(1, 4))
    assert brick.box.bottom_left_corner == Point(1, 4)
    assert brick.box.length == 100
    assert brick.box.height == 50
    assert not brick.is_built


def test_create_quarter_brick():
    brick = Brick.create_quarter_brick(Point(1, 4))
    assert brick.box.bottom_left_corner == Point(1, 4)
    assert brick.box.length == 45
    assert brick.box.height == 50
    assert not brick.is_built


def test_create_head_joint():
    head_joint = HeadJoint.create_head_joint(Point(2, 3))
    assert head_joint.box.bottom_left_corner == Point(2, 3)
    assert head_joint.box.length == 10
    assert head_joint.box.height == 50
    assert not head_joint.is_built


def test_unit_is_supported_when_first_course():
    brick = Brick.create_full_brick(Point(0, 0))
    assert brick.is_supported(None)


def test_unit_is_supported_when_both_below_not_built():
    brick = Brick.create_full_brick(Point(100, 62.5))
    irrelevant_built_brick = Brick.create_full_brick(Point(500, 0))
    irrelevant_built_brick.is_built = True
    course_below = Course(
        0,
        [
            Brick.create_full_brick(Point(0, 0)),
            Brick.create_full_brick(Point(220, 0)),
            irrelevant_built_brick,
        ],
    )
    assert not brick.is_supported(course_below)


def test_unit_is_supported_when_one_below_not_built():
    brick = Brick.create_full_brick(Point(100, 62.5))
    built_brick = Brick.create_full_brick(Point(0, 0))
    built_brick.is_built = True
    course_below = Course(0, [built_brick, Brick.create_full_brick(Point(220, 0))])
    assert not brick.is_supported(course_below)


def test_unit_is_supported_when_all_below_built():
    brick = Brick.create_full_brick(Point(100, 62.5))
    built_brick = Brick.create_full_brick(Point(0, 0))
    built_brick.is_built = True
    built_brick_2 = Brick.create_full_brick(Point(220, 0))
    built_brick_2.is_built = True
    course_below = Course(
        0, [built_brick, built_brick_2, Brick.create_full_brick(Point(500, 0))]
    )
    assert brick.is_supported(course_below)


def test_course_index():
    assert Course(0, []).index == 0
    assert Course(62.5, []).index == 1


def test_course_is_built_when_some_units_are_not():
    built_brick = Brick.create_full_brick(Point(0, 0))
    built_brick.is_built = True
    course = Course(
        0,
        [
            built_brick,
            Brick.create_full_brick(Point(220, 0)),
        ],
    )
    assert not course.is_built()


def test_course_is_built_when_all_units_built():
    built_brick = Brick.create_full_brick(Point(0, 0))
    built_brick.is_built = True
    head_joint = HeadJoint.create_head_joint(Point(210, 0))
    head_joint.is_built = True
    built_brick_2 = Brick.create_full_brick(Point(220, 0))
    built_brick_2.is_built = True
    course = Course(0, [built_brick, head_joint, built_brick_2])
    assert course.is_built()
    assert course.is_built()  # test it caches correct value


def test_wall_next_non_complete_course_when_not_yet_started():
    first_course = Course(0, [Brick.create_full_brick(Point(0, 0))])
    wall = Wall(
        Rectangle(Point(0, 0), 10, 500),
        [first_course, Course(62.5, [Brick.create_full_brick(Point(0, 62.5))])],
    )
    assert wall.next_non_complete_course() is first_course


def test_wall_next_non_complete_course_when_started():
    built_brick = Brick.create_full_brick(Point(0, 0))
    built_brick.is_built = True
    second_course = Course(62.5, [Brick.create_full_brick(Point(0, 62.5))])
    wall = Wall(
        Rectangle(Point(0, 0), 10, 500), [Course(0, [built_brick]), second_course]
    )
    assert wall.next_non_complete_course() is second_course


def test_wall_next_non_complete_course_when_finished():
    built_brick = Brick.create_full_brick(Point(0, 0))
    built_brick.is_built = True
    wall = Wall(
        Rectangle(Point(0, 0), 10, 500),
        [Course(0, [built_brick]), Course(62.5, [built_brick])],
    )
    assert wall.next_non_complete_course() is None
    assert wall.next_non_complete_course() is None  # test it caches correct value


def test_stretcher_bond_when_first_brick_on_even_course():
    bond = StretcherBond()
    brick = bond.next_brick_in_course([], 2, Point(0, 0), 2300)
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == FULL_BRICK_LENGTH


def test_stretcher_bond_when_last_brick_on_even_course():
    bond = StretcherBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 0, Point(2200, 0), 2300
    )
    assert brick.box.bottom_left_corner == Point(2200, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_stretcher_bond_when_first_brick_on_odd_course():
    bond = StretcherBond()
    brick = bond.next_brick_in_course([], 3, Point(0, 0), 2300)
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_stretcher_bond_when_last_brick_on_odd_course():
    bond = StretcherBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 1, Point(2090, 0), 2300
    )
    assert brick.box.bottom_left_corner == Point(2090, 0)
    assert brick.box.length == FULL_BRICK_LENGTH


def test_stretcher_bond_when_middle_brick():
    bond = StretcherBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 1, Point(300, 0), 2300
    )
    assert brick.box.bottom_left_corner == Point(300, 0)
    assert brick.box.length == FULL_BRICK_LENGTH


def test_create_stretcher_wall():
    wall = create_wall(2300, 2000, StretcherBond())
    assert len(wall.courses) == 32
    for i in range(32):
        units = wall.courses[i].units
        assert len(units) == 21
        assert units.pop(0 if i % 2 == 1 else -1).box.length == HALF_BRICK_LENGTH
        assert units.pop(0 if i % 2 == 1 else -1).box.length == HEAD_JOINT_THICKNESS
        for j, unit in enumerate(units):
            if j % 2 == 0:
                assert unit.box.length == FULL_BRICK_LENGTH
            else:
                assert unit.box.length == HEAD_JOINT_THICKNESS


def test_cross_bond_when_first_brick_on_even_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course([], 2, Point(0, 0), 2300)
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == QUARTER_BRICK_LENGTH


def test_cross_bond_when_middle_brick_on_even_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 0, Point(500, 0), 2300
    )
    assert brick.box.bottom_left_corner == Point(500, 0)
    assert brick.box.length == FULL_BRICK_LENGTH


def test_cross_bond_when_last_brick_on_even_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 4, Point(2255, 0), 2300
    )
    assert brick.box.bottom_left_corner == Point(2255, 0)
    assert brick.box.length == QUARTER_BRICK_LENGTH


def test_cross_bond_when_first_brick_on_odd_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course([], 1, Point(0, 0), 2300)
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_cross_bond_when_middle_brick_on_odd_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 3, Point(500, 0), 2300
    )
    assert brick.box.bottom_left_corner == Point(500, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_cross_bond_when_last_brick_on_odd_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 5, Point(2200, 0), 2300
    )
    assert brick.box.bottom_left_corner == Point(2200, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_create_cross_wall():
    wall = create_wall(2300, 2000, CrossBond())
    assert len(wall.courses) == 32
    for i in range(0, 32, 2):
        units = wall.courses[i].units
        assert len(units) == 23
        assert units.pop(0).box.length == QUARTER_BRICK_LENGTH
        last_brick = units.pop(-1)
        assert last_brick.box.length == QUARTER_BRICK_LENGTH
        assert last_brick.box.bottom_left_corner.x + QUARTER_BRICK_LENGTH == 2300
        for j, unit in enumerate(units):
            if j % 2 == 0:
                assert unit.box.length == HEAD_JOINT_THICKNESS
            else:
                assert unit.box.length == FULL_BRICK_LENGTH
    for i in range(1, 32, 2):
        units = wall.courses[i].units
        assert len(units) == 41
        for j, unit in enumerate(units):
            if j % 2 == 0:
                assert unit.box.length == HALF_BRICK_LENGTH
            else:
                assert unit.box.length == HEAD_JOINT_THICKNESS
        assert units[-1].box.bottom_left_corner.x + HALF_BRICK_LENGTH == 2300


def test_create_flemish_wall():
    wall = create_wall(2300, 2000, FlemishBond())
    assert len(wall.courses) == 32
    for i in range(0, 32, 2):
        units = wall.courses[i].units
        assert len(units) == 27
        for j, unit in enumerate(units):
            if j % 2 == 0:
                if j % 4 == 0:
                    assert unit.box.length == HALF_BRICK_LENGTH
                else:
                    assert unit.box.length == FULL_BRICK_LENGTH
            else:
                assert unit.box.length == HEAD_JOINT_THICKNESS
        last_brick = units[-1]
        assert last_brick.box.bottom_left_corner.x + last_brick.box.length == 2300
    for i in range(1, 32, 2):
        units = wall.courses[i].units
        assert len(units) == 29
        assert units.pop(0).box.length == THREE_QUARTER_BRICK_LENGTH
        last_brick = units.pop(-1)
        assert last_brick.box.length == QUARTER_BRICK_LENGTH
        assert last_brick.box.bottom_left_corner.x + last_brick.box.length == 2300
        for j, unit in enumerate(units):
            if j % 2 == 0:
                assert unit.box.length == HEAD_JOINT_THICKNESS
            else:
                if j % 4 == 1:
                    assert unit.box.length == HALF_BRICK_LENGTH
                else:
                    assert unit.box.length == FULL_BRICK_LENGTH
