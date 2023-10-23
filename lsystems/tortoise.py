"""Class implementing turtle"""
import numpy as np


class Tortoise:
    def __init__(self):
        self.pos = np.array([0, 0])
        self.angle_deg = 0.0
        self.d = 1.0

    def get_angle_rad(self):
        return self.angle_deg * np.pi / 180

    def forward(self):
        x, y = self.pos[0], self.pos[1]
        new_x = x + self.d * np.cos(self.get_angle_rad())
        new_y = y + self.d * np.sin(self.get_angle_rad())

        self.pos = np.array([new_x, new_y])

    def rotate(self, deg):
        self.angle_deg += deg
