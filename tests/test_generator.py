import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
from lsystems.generator import Generator
from lsystems.lsys import Lsys

alphabet = ["A", "B"]
rules = {"A": "AB", "B": "AA"}
test_lsys = Lsys(alphabet, rules)
test_gen = Generator(test_lsys, "A", 3)

test_lsys1 = Lsys(["F", "f", "+", "-"], {"F": "F-F+F"})
test_gen1 = Generator(test_lsys1, "F-F", 1)


def test_generate():
    steps = test_gen.generate()
    assert steps[-1] == "ABAAABAB"


def test_generate_tortoise_steps():
    steps, _ = test_gen1.generate_tortoise()
    steps_expectation = ["F-F", "F-F+F-F-F+F"]
    assert steps == steps_expectation


def test_generate_tortoise_history():
    _, history = test_gen1.generate_tortoise()
    print(history)
    history_expectation = [
        [
            np.array([0, 0]),
            np.array([1, 0]),
            np.array([1, -1]),
            np.array([2, -1]),
            np.array([2, -2]),
            np.array([1, -2]),
            np.array([1, -3]),
        ]
    ]
    print(history_expectation)
    assert_allclose(history, history_expectation)
