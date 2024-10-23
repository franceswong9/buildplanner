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
        return self.bounds_point(other.bottom_left_corner) and self.bounds_point(
            other.top_right_corner
        )

    def overlaps_in_x_axis(self, other: Rectangle) -> bool:
        return not (
            self.bottom_right_corner.x < other.bottom_left_corner.x
            or self.bottom_left_corner.x > other.bottom_right_corner.x
        )

    def bounds_point(self, point: Point) -> bool:
        return self.bounds_x(point.x) and self.bounds_y(point.y)

    def bounds_x(self, x: float) -> bool:
        return self.bottom_left_corner.x <= x <= self.bottom_right_corner.x

    def bounds_y(self, y: float) -> bool:
        return self.bottom_left_corner.y <= y <= self.top_left_corner.y

    def slice_at_x(self, x: float) -> Rectangle:
        if x - self.bottom_left_corner.x < 0:
            raise ValueError("Cannot have negative length rectangle")
        return Rectangle(
            self.bottom_left_corner,
            min(self.length, x - self.bottom_left_corner.x),
            self.height,
        )
