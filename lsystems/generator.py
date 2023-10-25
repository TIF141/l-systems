import numpy as np
from lsystems.tortoise import Tortoise


class Generator:
    def __init__(self, lsys, axiom, branching_angle, nsteps):
        self.lsys = lsys
        self.axiom = axiom
        self.branching_angle = branching_angle
        self.nsteps = nsteps
        self.stack = []

    def generate(self):
        predecessors = self.axiom
        steps = [self.axiom]
        for _ in range(self.nsteps):
            successors = self.lsys.step(predecessors)
            predecessors = successors
            steps.append(successors)
        return steps

    def generate_tortoise(self):
        predecessors = self.axiom
        steps = [self.axiom]
        tort = Tortoise()
        for _ in range(self.nsteps):
            successors = self.lsys.step(predecessors)
            predecessors = successors
            steps.append(successors)
            for successor in successors:
                if successor == "F":
                    tort.forward(draw=True)
                if successor == "-":
                    tort.rotate(-self.branching_angle)
                if successor == "+":
                    tort.rotate(self.branching_angle)
                if successor == "[":
                    self.stack.append(np.array([*tort.pos, tort.angle_deg]))
                if successor == "]":
                    root = self.stack.pop(-1)
                    tort.pos = root[:2]
                    tort.angle_deg = root[2]
                    tort.prev_draw = False
        return steps, tort.get_history(), self.stack


if __name__ == "__main__":
    from lsys import Lsys
    from draw import draw_coords

    # test_lsys = Lsys(["A", "B"], {"A": "AB"})
    # test_lsys.add_rules({"B": "AA"})

    # test_generator = Generator(test_lsys, "A", 10)
    # print(test_generator.generate())
    # test_lsys = Lsys(["F", "f", "+", "-"], {"F": "F-F+F+FF-F-F+F"})
    # test_lsys = Lsys(["F", "f", "+", "-"], {"F": "F-F+F"})
    # test_gen = Generator(test_lsys, "F-F-F-F", 90, 4)
    test_alphabet = ["F", "f", "+", "-", "[", "]"]
    test_dict = {"F": "FF-[-F+F+F]+[+F-F-F]"}
    test_lsys = Lsys(test_alphabet, test_dict)
    test_gen = Generator(test_lsys, "F", 22.5, 4)
    steps, history, stack = test_gen.generate_tortoise()
    # print(steps)
    for i in stack:
        print(i)
    print(history)
    draw_coords(history, 500)
