"""Class implementing turtle"""
import numpy as np


class Tortoise:
    def __init__(self):
        self.pos = np.array([0, 0])
        self.angle_deg = 0.0
        self.d = 1.0
        self.history = []
        self.prev_draw = False

    def get_angle_rad(self):
        return self.angle_deg * np.pi / 180

    def forward(self, draw=True):
        # if starting new chunk
        if draw and not self.prev_draw:
            self.history.append([])
            self.update_history()
            self.prev_draw = True

        x, y = self.pos[0], self.pos[1]
        new_x = x + self.d * np.cos(self.get_angle_rad())
        new_y = y + self.d * np.sin(self.get_angle_rad())

        self.pos = np.array([new_x, new_y])

        if draw:
            self.update_history()
        else:
            self.prev_draw = False

    def rotate(self, deg):
        self.angle_deg += deg

    def update_history(self):
        self.history[-1].append(self.pos)

    def get_history(self):
        return self.history


if __name__ == "__main__":
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
    print(h)
    from lsystems.draw import draw_coords

    draw_coords(h, 200)
