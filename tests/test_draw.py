import numpy as np
from numpy.testing import assert_array_equal
from lsystems.draw import get_extent


def test_width():
    test_coords = [np.array([[0, 0], [10, 4]]), np.array([[1, 2], [4, 9]])]

    width, height, max_points, min_points = get_extent(test_coords)

    assert width == 10


def test_height():
    test_coords = [np.array([[0, 0], [10, 4]]), np.array([[1, 2], [4, 9]])]

    width, height, max_points, min_points = get_extent(test_coords)

    assert height == 9


def test_max_points():
    test_coords = [np.array([[0, 0], [10, 4]]), np.array([[1, 2], [4, 9]])]

    width, height, max_points, min_points = get_extent(test_coords)

    assert_array_equal(max_points, np.array([10, 9]))


def test_min_points():
    test_coords = [np.array([[0, 0], [10, 4]]), np.array([[1, 2], [4, 9]])]

    width, height, max_points, min_points = get_extent(test_coords)

    assert_array_equal(min_points, np.array([0, 0]))


def test_max_points_one_chunk():
    test_coords = [np.array([[0, 0], [10, 0], [1, 1]])]

    width, height, max_points, min_points = get_extent(test_coords)

    assert_array_equal(max_points, np.array([10, 1]))


def test_min_points_one_chunk():
    test_coords = [np.array([[0, 0], [10, 0], [1, -5]])]

    width, height, max_points, min_points = get_extent(test_coords)

    assert_array_equal(min_points, np.array([0, -5]))
