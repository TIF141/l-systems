"""Class implementing turtle"""
import numpy as np


class Tortoise:
    def __init__(self):
        self.pos = np.array([0, 0])
        self.angle = 0.0
        self.d = 1.0

    def forward(self):
        x, y = self.pos[0], self.pos[1]
        new_x = x + self.d * np.cos(self.angle)
        new_y = y + self.d * np.sin(self.angle)

        self.pos = np.array([new_x, new_y])
