from __future__ import annotations

import random
from _operator import itemgetter

from typing import List, Literal

from buildplanner.util import Point, Rectangle
from buildplanner.model import (
    Unit,
    Course,
    Brick,
    FULL_BRICK_LENGTH,
    HALF_BRICK_LENGTH,
    QUARTER_BRICK_LENGTH,
    HEAD_JOINT_THICKNESS,
    COURSE_HEIGHT,
    BED_JOINT_THICKNESS,
    HeadJoint,
    Wall,
)


class Bond:
    def next_brick_in_course(
        self,
        course: List[Unit],
        course_idx: int,
        bottom_left_corner: Point,
        wall_length: float,
        previous_courses: List[Course],
    ) -> Brick:
        raise NotImplementedError

    @staticmethod
    def retries() -> int:
        return 0

    @staticmethod
    def is_first_brick(bricks: List[Unit]) -> bool:
        return len(bricks) == 0

    @staticmethod
    def is_odd_course(index: int) -> bool:
        return index % 2 == 1

    @staticmethod
    def is_full_brick_too_long(point: Point, length: float) -> bool:
        return point.x + FULL_BRICK_LENGTH > length

    @staticmethod
    def is_prev_half_brick(course: List[Unit]) -> bool:
        return len(course) >= 2 and course[-2].box.length == HALF_BRICK_LENGTH

    @staticmethod
    def fit_brick_at_end(candidate_brick: Brick, wall_length: float) -> Brick:
        # assumes that we have a wall length that perfectly fits our pre-sized bricks
        # i.e. this won't create anything other than full, three-quarter, half and quarter bricks
        return Brick(candidate_brick.box.slice_at_x(wall_length))


class StretcherBond(Bond):
    def next_brick_in_course(
        self,
        course: List[Unit],
        course_idx: int,
        bottom_left_corner: Point,
        wall_length: float,
        previous_courses: List[Course],
    ) -> Brick:
        if self.is_first_brick(course) and self.is_odd_course(course_idx):
            return Brick.create_half_brick(bottom_left_corner)
        return self.fit_brick_at_end(
            Brick.create_full_brick(bottom_left_corner), wall_length
        )


class CrossBond(Bond):
    def next_brick_in_course(
        self,
        course: List[Unit],
        course_idx: int,
        bottom_left_corner: Point,
        wall_length: float,
        previous_courses: List[Course],
    ) -> Brick:
        if self.is_odd_course(course_idx):
            return Brick.create_half_brick(bottom_left_corner)
        if self.is_first_brick(course):
            return Brick.create_quarter_brick(bottom_left_corner)
        return self.fit_brick_at_end(
            Brick.create_full_brick(bottom_left_corner), wall_length
        )


class FlemishBond(Bond):
    def next_brick_in_course(
        self,
        course: List[Unit],
        course_idx: int,
        bottom_left_corner: Point,
        wall_length: float,
        previous_courses: List[Course],
    ) -> Brick:
        if self.is_first_brick(course):
            if self.is_odd_course(course_idx):
                return Brick.create_three_quarter_brick(bottom_left_corner)
            return Brick.create_half_brick(bottom_left_corner)
        next_brick = (
            Brick.create_full_brick(bottom_left_corner)
            if self.is_prev_half_brick(course)
            else Brick.create_half_brick(bottom_left_corner)
        )
        return self.fit_brick_at_end(next_brick, wall_length)


class WallPlanningException(Exception):
    pass


class WildBond(Bond):
    MAX_PATTERN_LENGTH = 6
    CHECK_DISTANCE = QUARTER_BRICK_LENGTH + HEAD_JOINT_THICKNESS

    @staticmethod
    def retries() -> int:
        return 20

    def next_brick_in_course(
        self,
        course: List[Unit],
        course_idx: int,
        bottom_left_corner: Point,
        wall_length: float,
        previous_courses: List[Course],
    ) -> Brick:
        candidate_bricks = self._candidate_bricks(
            bottom_left_corner, course, course_idx
        )
        random.shuffle(candidate_bricks)
        bricks_with_pattern_length = [
            (b, self._length_of_longest_pattern(previous_courses, b))
            for b in candidate_bricks
        ]
        best_brick, pattern_length = min(bricks_with_pattern_length, key=itemgetter(1))
        if pattern_length >= self.MAX_PATTERN_LENGTH:
            raise WallPlanningException("We planned a wall with too many stairs/teeth")
        return self.fit_brick_at_end(best_brick, wall_length)

    def _candidate_bricks(
        self, bottom_left_corner: Point, course: List[Unit], course_idx: int
    ) -> List[Brick]:
        if self.is_first_brick(course) and self.is_odd_course(course_idx):
            return [
                Brick.create_quarter_brick(bottom_left_corner),
                Brick.create_three_quarter_brick(bottom_left_corner),
            ]
        elif self.is_prev_half_brick(course):
            return [Brick.create_full_brick(bottom_left_corner)]
        return [
            Brick.create_full_brick(bottom_left_corner),
            Brick.create_half_brick(bottom_left_corner),
        ]

    def _length_of_longest_pattern(
        self, previous_courses: List[Course], potential_brick: Brick
    ) -> int:
        return max(
            [
                self._length_of_pattern(
                    previous_courses, potential_brick, direction, direction_multiplier
                )
                for direction in (1, -1)
                for direction_multiplier in (1, -1)
            ]
        )

    def _length_of_pattern(
        self,
        previous_courses: List[Course],
        potential_brick: Brick,
        direction: Literal[1, -1],
        direction_multiplier: Literal[1, -1],
    ) -> int:
        check_x = potential_brick.box.bottom_right_corner.x
        i = 0
        for i in range(1, min(len(previous_courses), self.MAX_PATTERN_LENGTH) + 1):
            check_x += direction * self.CHECK_DISTANCE
            if not previous_courses[-i].joint_exists_at(check_x):
                return i - 1
            direction *= direction_multiplier
        return i


def _create_course(
    index: int, length: float, bond: Bond, previous_courses: List[Course]
) -> Course:
    units = []
    point = Point(0, index * COURSE_HEIGHT + BED_JOINT_THICKNESS)
    while point.x < length:
        brick = bond.next_brick_in_course(units, index, point, length, previous_courses)
        units.append(brick)
        point = point.plus_x(brick.box.length)

        if point.x < length:
            units.append(HeadJoint.create_head_joint(point))
            point = point.plus_x(HEAD_JOINT_THICKNESS)
    return Course(index * COURSE_HEIGHT, units)


def create_wall(length: float, height: float, bond: Bond) -> Wall:
    retries = bond.retries()
    while retries >= 0:
        try:
            box = Rectangle(Point(0, 0), length, height)
            number_of_courses = int(height / COURSE_HEIGHT)
            courses = []
            for i in range(number_of_courses):
                courses.append(_create_course(i, length, bond, courses))
            return Wall(box, courses)
        except WallPlanningException:
            retries -= 1
    raise WallPlanningException(
        f"Couldn't plan a wall that satisfied the rules of bond type: {bond.__class__.__name__}"
    )
