import numpy as np
import os
from numpy.testing import assert_array_equal
from lsystems.draw import get_extent, draw_coords
from lsystems.tortoise import Tortoise
from lsystems.generator import Generator
from lsystems.lsys import Lsys
from PIL import Image, ImageChops


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


def test_image_generated(tmp_path):
    t = Tortoise()
    t.forward()
    t.rotate(45)
    t.forward()
    t.forward(draw=False)
    t.forward(draw=False)
    t.forward()
    t.rotate(75)
    t.forward()
    t.forward()
    t.rotate(10)
    t.forward(draw=False)
    t.forward(draw=False)
    t.forward()
    t.forward()
    t.forward()
    t.forward()
    t.forward()
    h = t.get_history()

    grid = draw_coords(h, 200)

    path = os.path.join(tmp_path, "image.jpg")
    im = Image.fromarray(grid)
    im.save(path)

    correct_im = Image.open("tests/test_imgs/test_tortoise_draw.jpg")
    saved_im = Image.open(path)
    diff = ImageChops.difference(correct_im, saved_im)

    assert not diff.getbbox()


def test_multiple_iterations_draw(tmp_path):
    """ "From pg 10, Fig. 1.9(a)."""
    alphabet = ["F", "f", "+", "-"]
    rules = {"F": "FF-F-F-F-F-F+F"}
    axiom = "F-F-F-F"
    angle = 90
    iterations = 4
    lsys = Lsys(alphabet, rules)
    g = Generator(lsys, axiom, angle, iterations)
    _, history, _ = g.generate_tortoise()
    grid = draw_coords(history, 200)
    path = os.path.join(tmp_path, "image.jpg")
    im = Image.fromarray(grid)
    im.save(path)
    correct_im = Image.open("tests/test_imgs/test_tortoise_iterations_draw.jpg")
    saved_im = Image.open(path)
    diff = ImageChops.difference(correct_im, saved_im)

    assert not diff.getbbox()


def test_branching_draw(tmp_path):
    """From pg 25, Fig. 1.24(a)."""
    alphabet = ["F", "f", "+", "-"]
    rules = {"F": "F[+F]F[-F]F"}
    axiom = "F"
    angle = 27.5
    iterations = 5
    lsys = Lsys(alphabet, rules)
    g = Generator(lsys, axiom, angle, iterations)
    _, history, _ = g.generate_tortoise()
    grid = draw_coords(history, 200)
    path = os.path.join(tmp_path, "image.jpg")
    im = Image.fromarray(grid)
    im.save(path)

    correct_im = Image.open("tests/test_imgs/test_tortoise_branching_draw.jpg")
    saved_im = Image.open(path)
    diff = ImageChops.difference(correct_im, saved_im)

    assert not diff.getbbox()


def test_branching_multiple_rules(tmp_path):
    """From pg 25, Fig. 1.24(d)."""
    alphabet = ["F", "f", "+", "-"]
    rules = {"X": "F[+X]F[-X]+X", "F": "FF"}
    axiom = "X"
    angle = 20
    iterations = 7
    lsys = Lsys(alphabet, rules)
    g = Generator(lsys, axiom, angle, iterations)
    _, history, _ = g.generate_tortoise()
    grid = draw_coords(history, 200)
    path = os.path.join(tmp_path, "image.jpg")
    im = Image.fromarray(grid)
    im.save(path)

    correct_im = Image.open("tests/test_imgs/test_tortoise_multiple_rules.jpg")
    saved_im = Image.open(path)
    diff = ImageChops.difference(correct_im, saved_im)

    assert not diff.getbbox()


if __name__ == "__main__":
    # test_image_generated("")
    # test_multiple_iterations_draw("")
    # test_branching_draw("")
    # test_branching_multiple_rules("")
    pass
