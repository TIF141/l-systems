from lsystems.tortoise import Tortoise
from numpy.testing import assert_equal, assert_array_equal
import numpy as np


def test_initial_pos():
    tortoise = Tortoise()
    assert_array_equal(tortoise.pos, np.array([0, 0]))


def test_initial_angle():
    tortoise = Tortoise()
    assert_equal(tortoise.angle, 0)


def test_forward():
    tortoise = Tortoise()
    tortoise.forward()
    assert_array_equal(tortoise.pos, np.array([1, 0]))
