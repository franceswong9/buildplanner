from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def plus_x(self, distance: float) -> Point:
        return Point(self.x + distance, self.y)

    def plus_y(self, distance: float) -> Point:
        return Point(self.x, self.y + distance)


@dataclass(frozen=True)
class Rectangle:
    bottom_left_corner: Point
    length: float
    height: float

    @property
    def top_left_corner(self) -> Point:
        return self.bottom_left_corner.plus_y(self.height)

    @property
    def bottom_right_corner(self) -> Point:
        return self.bottom_left_corner.plus_x(self.length)

    @property
    def top_right_corner(self) -> Point:
        return self.bottom_left_corner.plus_x(self.length).plus_y(self.height)

    @property
    def middle(self) -> Point:
        return self.bottom_left_corner.plus_x(self.length / 2).plus_y(self.height / 2)

    def bounds(self, other: Rectangle) -> bool:
        return self._bounds_point(other.bottom_left_corner) and self._bounds_point(
            other.top_right_corner
        )

    def overlaps_in_x_axis(self, other: Rectangle) -> bool:
        return not (
            self.bottom_right_corner.x < other.bottom_left_corner.x
            or self.bottom_left_corner.x > other.bottom_right_corner.x
        )

    def _bounds_point(self, point: Point) -> bool:
        return self._bounds_x(point) and self._bounds_y(point)

    def _bounds_x(self, point: Point) -> bool:
        return self.bottom_left_corner.x <= point.x <= self.bottom_right_corner.x

    def _bounds_y(self, point: Point) -> bool:
        return self.bottom_left_corner.y <= point.y <= self.top_left_corner.y
