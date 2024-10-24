from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

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

    def joint_exists_at(self, x: float) -> bool:
        for unit in self.units:
            if unit.box.bottom_left_corner.x == x and isinstance(unit, HeadJoint):
                return True
        return False


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
