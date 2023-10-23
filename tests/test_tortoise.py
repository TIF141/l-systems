from lsystems.tortoise import Tortoise
from numpy.testing import assert_equal, assert_array_equal


def test_initial():
    tortoise = Tortoise()
    assert tortoise.pos == [0, 0]


def test_forward():
    tortoise = Tortoise()
