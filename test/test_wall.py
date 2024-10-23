from buildplanner.util import Point, Rectangle
from buildplanner.wall import (
    Brick,
    Course,
    Wall,
    create_stretcher_wall,
    HeadJoint,
    HALF_BRICK_LENGTH,
    FULL_BRICK_LENGTH,
    HEAD_JOINT_THICKNESS,
)


def test_create_full_brick():
    brick = Brick.create_full_brick(Point(0, 0))
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == 210
    assert brick.box.height == 50
    assert not brick.is_built


def test_create_half_brick():
    brick = Brick.create_half_brick(Point(1, 4))
    assert brick.box.bottom_left_corner == Point(1, 4)
    assert brick.box.length == 100
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


def test_create_stretcher_wall():
    wall = create_stretcher_wall(2300, 2000)
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
