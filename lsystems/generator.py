import numpy as np
from tortoise import Tortoise


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
        from lsystems.tortoise import Tortoise

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

    def generate_tortoise_contextdep(self):
        predecessors = self.axiom
        steps = [self.axiom]
        tort = Tortoise()
        for _ in range(self.nsteps):
            print("#### Next step")
            successors = self.lsys.step_contextdep(predecessors)
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

    # test_lsys = Lsys(["F", "f", "+", "-", "[", "]"], {"F": "FF-[-F+F+F]+[+F-F-F]"})
    test_lsys = Lsys(
        ["F1", "F0", "+", "-", "[", "]"],
        {
            "0<0>0": "0",
            "0<0>1": "1[-F1F1]",
            "0<1>0": "1",
            "0<1>1": "1",
            "1<0>0": "0",
            "1<0>1": "1F1",
            "1<1>0": "1",
            "1<1>1": "0",
            "*<+>*": "-",
            "*<->*": "+",
        },
        "+-F",
    )
    test_gen = Generator(test_lsys, "F1F1F1", 22.5, 7)
    steps, history, stack = test_gen.generate_tortoise_contextdep()
    print(steps)
    draw_coords(history, 500)
