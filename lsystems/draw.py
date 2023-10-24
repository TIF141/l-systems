import numpy as np
from typing import List
from skimage.draw import line_aa
from PIL import Image


def get_extent(coords: List[np.ndarray]):
    """Gets the width and height of a figure given a (possibly discontinuous)
       set of coords.

    Args:
        coords (List[np.ndarray]): list of x and y values

    Returns:
        width, height (int, int): width and height of the drawing
    """
    # Get max and min coords
    max_points = np.array([np.max(ps, 0) for ps in coords])
    min_points = np.array([np.min(ps, 0) for ps in coords])

    # If more than one discontinuous group of coords
    if len(coords) > 1:
        max_points = np.max(max_points, 0)
        min_points = np.min(min_points, 0)
    else:
        # Expand interior list
        max_points = max_points[0]
        min_points = min_points[0]

    width, height = max_points - min_points

    return width, height, max_points, min_points


def draw_coords(coords, res: int, scale=True):
    grid = np.zeros((res, res))
    width, height, max_points, min_points = get_extent(coords)
    limiting_fac = max(width, height)
    scale_factor = (res - 1) / limiting_fac

    for ps in coords:
        ps = np.array(ps)
        ps -= min_points
        if scale:
            ps *= scale_factor
        for i, point in enumerate(ps[:-1]):
            next_p = ps[i + 1]
            rr, cc, val = line_aa(
                *np.round(point).astype(int), *np.round(next_p).astype(int)
            )
            grid[rr, cc] = val * 255

    im = Image.fromarray(grid)
    im = im.convert("L")
    im = im.save("image.jpg")
    return im
