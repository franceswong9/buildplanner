from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List

from .util import Rectangle, Point

FULL_BRICK_LENGTH = 210
HALF_BRICK_LENGTH = 100
THREE_QUARTER_BRICK_LENGTH = 155
QUARTER_BRICK_LENGTH = 45
BRICK_HEIGHT = 50
BED_JOINT_THICKNESS = 12.5
HEAD_JOINT_THICKNESS = 10
COURSE_HEIGHT = BED_JOINT_THICKNESS + BRICK_HEIGHT


@dataclass
class Unit:
    box: Rectangle
    is_built: bool = False

    def is_supported(self, course_below: Optional[Course]) -> bool:
        if course_below is None:
            return True
        for unit_below in course_below.units:
            if unit_below._supports(self) and not unit_below.is_built:
                return False
        return True

    def _supports(self, unit_on_course_above: Unit) -> bool:
        return self.box.overlaps_in_x_axis(unit_on_course_above.box)


class Brick(Unit):
    @staticmethod
    def create_full_brick(bottom_left_corner: Point) -> Brick:
        return Brick(Rectangle(bottom_left_corner, FULL_BRICK_LENGTH, BRICK_HEIGHT))

    @staticmethod
    def create_three_quarter_brick(bottom_left_corner: Point) -> Brick:
        return Brick(
            Rectangle(bottom_left_corner, THREE_QUARTER_BRICK_LENGTH, BRICK_HEIGHT)
        )

    @staticmethod
    def create_half_brick(bottom_left_corner: Point) -> Brick:
        return Brick(Rectangle(bottom_left_corner, HALF_BRICK_LENGTH, BRICK_HEIGHT))

    @staticmethod
    def create_quarter_brick(bottom_left_corner: Point) -> Brick:
        return Brick(Rectangle(bottom_left_corner, QUARTER_BRICK_LENGTH, BRICK_HEIGHT))


class HeadJoint(Unit):
    @staticmethod
    def create_head_joint(bottom_left_corner: Point) -> HeadJoint:
        return HeadJoint(
            Rectangle(bottom_left_corner, HEAD_JOINT_THICKNESS, BRICK_HEIGHT)
        )


@dataclass
class Course:
    height: float
    units: list[Unit]
    _is_built: bool = False

    @property
    def index(self) -> int:
        return int(self.height / COURSE_HEIGHT)

    def is_built(self) -> bool:
        if self._is_built:
            return True
        for unit in self.units:
            if not unit.is_built:
                return False
        self._is_built = True
        return True


@dataclass
class Wall:
    box: Rectangle
    courses: list[Course]
    _is_built: bool = False

    def next_non_complete_course(self) -> Optional[Course]:
        if self._is_built:
            return None
        for course in self.courses:
            if not course.is_built():
                return course
        self._is_built = True
        return None


class Bond:
    def next_brick_in_course(
        self, units: List[Unit], index: int, point: Point, length: float
    ) -> Brick:
        raise NotImplementedError

    @staticmethod
    def is_first_brick(bricks: List[Unit]) -> bool:
        return len(bricks) == 0

    @staticmethod
    def is_odd_course(index: int) -> bool:
        return index % 2 == 1

    @staticmethod
    def is_full_brick_too_long(point: Point, length: float) -> bool:
        return point.x + FULL_BRICK_LENGTH > length


class StretcherBond(Bond):
    def next_brick_in_course(
        self, units: List[Unit], index: int, point: Point, length: float
    ) -> Brick:
        if (
            self.is_first_brick(units) and self.is_odd_course(index)
        ) or self.is_full_brick_too_long(point, length):
            # assumes that we have a wall length that perfectly fits full & half bricks
            return Brick.create_half_brick(point)
        return Brick.create_full_brick(point)


class CrossBond(Bond):
    def next_brick_in_course(
        self, units: List[Unit], index: int, point: Point, length: float
    ) -> Brick:
        if self.is_odd_course(index):
            return Brick.create_half_brick(point)
        if self.is_first_brick(units) or self.is_full_brick_too_long(point, length):
            # assumes that we have a wall length that perfectly fits full & quarter bricks
            return Brick.create_quarter_brick(point)
        return Brick.create_full_brick(point)


class FlemishBond(Bond):
    def next_brick_in_course(
        self, units: List[Unit], index: int, point: Point, length: float
    ) -> Brick:
        if self.is_first_brick(units):
            if self.is_odd_course(index):
                return Brick.create_three_quarter_brick(point)
            return Brick.create_half_brick(point)
        previous_brick_is_half = units[-2].box.length == HALF_BRICK_LENGTH
        next_brick = (
            Brick.create_full_brick(point)
            if previous_brick_is_half
            else Brick.create_half_brick(point)
        )
        if point.x + next_brick.box.length > length:
            # assumes that we have a wall that will perfectly fit these bricks
            next_brick = Brick.create_quarter_brick(point)
        return next_brick


def _create_course(index: int, length: float, bond: Bond) -> Course:
    units = []
    point = Point(0, index * COURSE_HEIGHT + BED_JOINT_THICKNESS)
    while point.x < length:
        brick = bond.next_brick_in_course(units, index, point, length)
        units.append(brick)
        point = point.plus_x(brick.box.length)

        if point.x < length:
            units.append(HeadJoint.create_head_joint(point))
            point = point.plus_x(HEAD_JOINT_THICKNESS)
    return Course(index * COURSE_HEIGHT, units)


def create_wall(length: float, height: float, bond: Bond) -> Wall:
    box = Rectangle(Point(0, 0), length, height)
    number_of_courses = int(height / COURSE_HEIGHT)
    return Wall(
        box, [_create_course(i, length, bond) for i in range(number_of_courses)]
    )
