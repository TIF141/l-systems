from lsystems.tortoise import Tortoise
from numpy.testing import assert_array_equal, assert_allclose
import numpy as np


def test_initial_pos():
    tortoise = Tortoise()
    assert_array_equal(tortoise.pos, np.array([0, 0]))


def test_initial_angle():
    tortoise = Tortoise()
    assert np.isclose(tortoise.get_angle_rad(), float(0))


def test_forward():
    tortoise = Tortoise()
    tortoise.forward()
    assert_array_equal(tortoise.pos, np.array([1, 0]))


def test_rotate():
    tortoise = Tortoise()
    angle_deg = 90
    tortoise.rotate(angle_deg)
    angle_rad = tortoise.get_angle_rad()
    assert np.isclose(tortoise.get_angle_rad(), angle_rad)


def test_rotate_and_move():
    tortoise = Tortoise()
    angle_deg = 45
    tortoise.rotate(angle_deg)
    tortoise.forward()
    assert_allclose(tortoise.pos, np.array([1 / np.sqrt(2), 1 / np.sqrt(2)]))


def test_history_empty():
    tortoise = Tortoise()
    assert_array_equal(tortoise.get_history(), np.array([]))


def test_history_draw():
    tortoise = Tortoise()
    tortoise.forward(draw=True)
    assert_allclose(tortoise.get_history(), np.array([[0, 0], [1, 0]]))


def test_history_nodraw_then_draw():
    tortoise = Tortoise()
    tortoise.forward(draw=False)
    tortoise.forward(draw=True)
    assert_allclose(tortoise.get_history(), np.array([[1, 0], [2, 0]]))
