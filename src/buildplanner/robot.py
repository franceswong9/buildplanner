from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Optional, Iterable

from .util import Rectangle, Point
from .model import Wall, Brick, Course, BED_JOINT_THICKNESS, Unit


class AlignmentStrategy:
    def next_reachable_area(self, unit: Unit, robot: Robot, wall: Wall) -> Rectangle:
        max_x = wall.box.length - robot.reachable_area.length
        max_y = wall.box.height - robot.reachable_area.height

        next_x = max(0.0, self.align_x_with_unit(unit, robot))
        next_x = min(next_x, max_x)
        next_y = min(unit.box.bottom_left_corner.y - BED_JOINT_THICKNESS, max_y)

        return Rectangle(
            Point(next_x, next_y),
            robot.reachable_area.length,
            robot.reachable_area.height,
        )

    def align_x_with_unit(self, unit: Unit, robot: Robot) -> float:
        raise NotImplementedError


class LeftAlignmentStrategy(AlignmentStrategy):
    def align_x_with_unit(self, unit: Unit, robot: Robot) -> float:
        return unit.box.bottom_left_corner.x


class RightAlignmentStrategy(AlignmentStrategy):
    def align_x_with_unit(self, unit: Unit, robot: Robot) -> float:
        return (
            unit.box.bottom_left_corner.x
            + unit.box.length
            - robot.reachable_area.length
        )


class CenterAlignmentStrategy(AlignmentStrategy):
    def align_x_with_unit(self, unit: Unit, robot: Robot) -> float:
        return (
            unit.box.bottom_left_corner.x
            + (unit.box.length / 2)
            - (robot.reachable_area.length / 2)
        )


class RandomAlignmentStrategy(AlignmentStrategy):
    def align_x_with_unit(self, unit: Unit, robot: Robot) -> float:
        unit_in_left_corner_x = LeftAlignmentStrategy().align_x_with_unit(unit, robot)
        unit_in_right_corner_x = RightAlignmentStrategy().align_x_with_unit(unit, robot)
        return random.uniform(unit_in_right_corner_x, unit_in_left_corner_x)


@dataclass
class MoveStrategy:
    alignment_strategy: AlignmentStrategy

    def next_move(self, robot: Robot, wall: Wall) -> Optional[Rectangle]:
        next_course = wall.next_non_complete_course()
        if next_course is None:
            return None

        for unit in self._next_units_in_order(next_course):
            if not unit.is_built:
                return self.alignment_strategy.next_reachable_area(unit, robot, wall)
        return None

    def _next_units_in_order(self, course: Course) -> Iterable[Unit]:
        raise NotImplementedError


class LeftToRightMoveStrategy(MoveStrategy):
    def _next_units_in_order(self, course: Course) -> Iterable[Unit]:
        return course.units


class OutsideInMoveStrategy(MoveStrategy):
    _from_left_side: bool = True

    def _next_units_in_order(self, course: Course) -> Iterable[Unit]:
        self._from_left_side = not self._from_left_side
        return course.units if self._from_left_side else reversed(course.units)


class SnakeMoveStrategy(MoveStrategy):
    _last_course_index: int = 0
    _from_left_side: bool = True

    def _next_units_in_order(self, course: Course) -> Iterable[Unit]:
        if course.index > self._last_course_index:
            self._from_left_side = not self._from_left_side
            self._last_course_index = course.index
        return course.units if self._from_left_side else reversed(course.units)


class DynamicSnakeMoveStrategy(SnakeMoveStrategy):
    def _next_units_in_order(self, course: Course) -> Iterable[Unit]:
        units = course.units
        left_non_built_unit = self._index_of_first_non_built_unit(units)
        right_non_built_unit = self._index_of_first_non_built_unit(reversed(units))
        if right_non_built_unit > left_non_built_unit:
            self.alignment_strategy = LeftAlignmentStrategy()
            return reversed(units)
        self.alignment_strategy = RightAlignmentStrategy()
        return units

    @staticmethod
    def _index_of_first_non_built_unit(units: Iterable[Unit]) -> int:
        for i, unit in enumerate(units):
            if not unit.is_built:
                return i


@dataclass
class Robot:
    reachable_area: Rectangle
    _move_strategy: MoveStrategy
    move_count: int = 0

    def __init__(
        self,
        reachable_area_length: int,
        reachable_area_height: int,
        move_strategy: MoveStrategy,
    ) -> None:
        self.reachable_area = Rectangle(
            Point(0, 0), reachable_area_length, reachable_area_height
        )
        self._move_strategy = move_strategy

    def lay_brick(self, wall: Wall) -> Optional[Brick]:
        for i, course in enumerate(wall.courses):
            previous_course = wall.courses[i - 1] if i > 0 else None
            for unit in course.units:
                if (
                    not unit.is_built
                    and self._reachable(unit)
                    and unit.is_supported(previous_course)
                ):
                    unit.is_built = True
                    if isinstance(unit, Brick):
                        return unit
        return None

    def _reachable(self, unit: Unit) -> bool:
        bed_joint_box = Rectangle(
            unit.box.bottom_left_corner.plus_y(-1 * BED_JOINT_THICKNESS),
            unit.box.length,
            BED_JOINT_THICKNESS,
        )
        return self.reachable_area.bounds(bed_joint_box) and self.reachable_area.bounds(
            unit.box
        )

    def move(self, wall: Wall) -> bool:
        next_move = self._move_strategy.next_move(self, wall)
        if next_move is None:
            return False
        self.reachable_area = next_move
        self.move_count += 1
        return True
