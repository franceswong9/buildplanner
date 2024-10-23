from buildplanner.util import Point
from buildplanner.model import (
    Brick,
    HALF_BRICK_LENGTH,
    FULL_BRICK_LENGTH,
    HEAD_JOINT_THICKNESS,
    QUARTER_BRICK_LENGTH,
    THREE_QUARTER_BRICK_LENGTH,
)
from buildplanner.wall import StretcherBond, CrossBond, FlemishBond, create_wall


def test_stretcher_bond_when_first_brick_on_even_course():
    bond = StretcherBond()
    brick = bond.next_brick_in_course([], 2, Point(0, 0), 2300, [])
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == FULL_BRICK_LENGTH


def test_stretcher_bond_when_last_brick_on_even_course():
    bond = StretcherBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 0, Point(2200, 0), 2300, []
    )
    assert brick.box.bottom_left_corner == Point(2200, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_stretcher_bond_when_first_brick_on_odd_course():
    bond = StretcherBond()
    brick = bond.next_brick_in_course([], 3, Point(0, 0), 2300, [])
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_stretcher_bond_when_last_brick_on_odd_course():
    bond = StretcherBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 1, Point(2090, 0), 2300, []
    )
    assert brick.box.bottom_left_corner == Point(2090, 0)
    assert brick.box.length == FULL_BRICK_LENGTH


def test_stretcher_bond_when_middle_brick():
    bond = StretcherBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 1, Point(300, 0), 2300, []
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
    brick = bond.next_brick_in_course([], 2, Point(0, 0), 2300, [])
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == QUARTER_BRICK_LENGTH


def test_cross_bond_when_middle_brick_on_even_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 0, Point(500, 0), 2300, []
    )
    assert brick.box.bottom_left_corner == Point(500, 0)
    assert brick.box.length == FULL_BRICK_LENGTH


def test_cross_bond_when_last_brick_on_even_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 4, Point(2255, 0), 2300, []
    )
    assert brick.box.bottom_left_corner == Point(2255, 0)
    assert brick.box.length == QUARTER_BRICK_LENGTH


def test_cross_bond_when_first_brick_on_odd_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course([], 1, Point(0, 0), 2300, [])
    assert brick.box.bottom_left_corner == Point(0, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_cross_bond_when_middle_brick_on_odd_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 3, Point(500, 0), 2300, []
    )
    assert brick.box.bottom_left_corner == Point(500, 0)
    assert brick.box.length == HALF_BRICK_LENGTH


def test_cross_bond_when_last_brick_on_odd_course():
    bond = CrossBond()
    brick = bond.next_brick_in_course(
        [Brick.create_full_brick(Point(0, 0))], 5, Point(2200, 0), 2300, []
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
