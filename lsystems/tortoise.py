"""Class implementing turtle"""
import numpy as np


class Tortoise:
    def __init__(self):
        self.pos = np.array([0, 0])
        self.angle_deg = 0.0
        self.d = 1.0
        self.history = []

    def get_angle_rad(self):
        return self.angle_deg * np.pi / 180

    def forward(self, draw=False):
        if draw:
            if len(self.get_history()) == 0:
                self.update_history()
            elif not self.get_history()[-1] == self.pos:
                self.update_history()

        x, y = self.pos[0], self.pos[1]
        new_x = x + self.d * np.cos(self.get_angle_rad())
        new_y = y + self.d * np.sin(self.get_angle_rad())

        self.pos = np.array([new_x, new_y])

        if draw:
            self.update_history()

    def rotate(self, deg):
        self.angle_deg += deg

    def update_history(self):
        self.history.append(self.pos)

    def get_history(self):
        return np.array(self.history)
