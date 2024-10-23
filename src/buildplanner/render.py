from typing import Optional

from .wall import Brick, Wall
from turtle import Turtle

FONT_HEIGHT_ADJUSTMENT = 10


class Renderer:
    def __init__(self) -> None:
        self._turtle = Turtle()
        self._turtle.hideturtle()
        self._turtle.penup()
        self._turtle.left(90)

    def render_wall(self, wall: Wall) -> None:
        for course in wall.courses:
            for unit in course.units:
                if isinstance(unit, Brick):
                    self.render_brick(unit, "LightGrey", None)

    def render_brick(self, brick: Brick, colour: str, stride: Optional[int]) -> None:
        self._turtle.goto(
            brick.box.bottom_left_corner.x, brick.box.bottom_left_corner.y
        )
        self._turtle.color(colour)
        self._turtle.pendown()

        self._turtle.begin_fill()
        self._turtle.goto(brick.box.top_left_corner.x, brick.box.top_left_corner.y)
        self._turtle.goto(brick.box.top_right_corner.x, brick.box.top_right_corner.y)
        self._turtle.goto(
            brick.box.bottom_right_corner.x, brick.box.bottom_right_corner.y
        )
        self._turtle.goto(
            brick.box.bottom_left_corner.x, brick.box.bottom_left_corner.y
        )
        self._turtle.end_fill()

        if stride is not None:
            self._turtle.color("black")
            self._turtle.penup()
            self._turtle.goto(
                brick.box.middle.x, brick.box.middle.y - FONT_HEIGHT_ADJUSTMENT
            )
            self._turtle.pendown()
            self._turtle.write(stride, align="center")

        self._turtle.penup()
