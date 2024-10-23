from buildplanner.util import Point, Rectangle


def test_point_plus_x():
    assert Point(1, -2).plus_x(3) == Point(4, -2)


def test_point_plus_x_when_negative():
    assert Point(1, 2).plus_x(-3) == Point(-2, 2)


def test_point_plus_y():
    assert Point(2, 4).plus_y(6) == Point(2, 10)


def test_point_plus_y_when_negative():
    assert Point(1, -2).plus_y(-3) == Point(1, -5)


def test_rectangle_top_left_corner():
    assert Rectangle(Point(1, -5), 2, 4).top_left_corner == Point(1, -1)


def test_rectangle_bottom_right_corner():
    assert Rectangle(Point(1, 1), 2, 6).bottom_right_corner == Point(3, 1)


def test_rectangle_top_right_corner():
    assert Rectangle(Point(-1, -2), 2, 6).top_right_corner == Point(1, 4)


def test_rectangle_middle():
    assert Rectangle(Point(-6, 4), 2, 2).middle == Point(-5, 5)


def test_rectangle_bounds_when_inside():
    assert Rectangle(Point(-10, -10), 20, 20).bounds(Rectangle(Point(0, 0), 5, 5))


def test_rectangle_bounds_when_on_border():
    assert Rectangle(Point(-5, 8), 3, 3).bounds(Rectangle(Point(-5, 8), 1, 1))


def test_rectangle_bounds_when_outside():
    assert not Rectangle(Point(0, 0), 20, 20).bounds(Rectangle(Point(5, -10), 1, 1))


def test_rectangle_bounds_when_partially_outside_left():
    assert not Rectangle(Point(0, 0), 20, 20).bounds(Rectangle(Point(-1, 0), 5, 5))


def test_rectangle_bounds_when_partially_outside_up_and_right():
    assert not Rectangle(Point(0, 0), 20, 20).bounds(Rectangle(Point(19, 19), 5, 5))


def test_rectangle_overlaps_in_x_axis_when_left_overlap():
    assert Rectangle(Point(0, 1), 5, 10).overlaps_in_x_axis(
        Rectangle(Point(3, -4), 3, 1)
    )


def test_rectangle_overlaps_in_x_axis_when_right_overlap():
    assert Rectangle(Point(5, 1), 3, 10).overlaps_in_x_axis(
        Rectangle(Point(3, -4), 3, 1)
    )


def test_rectangle_overlaps_in_x_axis_when_full_overlap_and_bigger():
    assert Rectangle(Point(5, 1), 5, 10).overlaps_in_x_axis(
        Rectangle(Point(6, -4), 1, 1)
    )


def test_rectangle_overlaps_in_x_axis_when_full_overlap_and_smaller():
    assert Rectangle(Point(5, 1), 5, 10).overlaps_in_x_axis(
        Rectangle(Point(0, -4), 20, 1)
    )


def test_rectangle_overlaps_in_x_axis_when_too_far_left():
    assert not Rectangle(Point(0, 1), 2, 10).overlaps_in_x_axis(
        Rectangle(Point(3, -4), 3, 1)
    )


def test_rectangle_overlaps_in_x_axis_when_too_far_right():
    assert not Rectangle(Point(7, 1), 2, 10).overlaps_in_x_axis(
        Rectangle(Point(3, -4), 3, 1)
    )
