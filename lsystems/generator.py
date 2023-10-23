from lsys import Lsys


class Generator:
    def __init__(self, lsys, axiom, nsteps):
        self.lsys = lsys
        self.axiom = axiom
        self.nsteps = nsteps

    def generate(self):
        predecessors = self.axiom
        for _ in range(self.nsteps):
            successors = self.lsys.step(predecessors)
            predecessors = successors
            print(successors)


if __name__ == "__main__":
    test_lsys = Lsys(["A", "B"], {"A": "AB"})
    test_lsys.add_rules({"B": "AA"})

    test_generator = Generator(test_lsys, "A", 4)
    test_generator.generate()
