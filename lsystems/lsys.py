class Lsys:
    def __init__(self, alphabet, rules):
        self.alphabet = alphabet
        self.rules = rules

    def add_rules(self, newrules):
        for predecessor, successor in newrules.items():
            self.rules[predecessor] = successor

    def step(self, predecessors, nsteps):
        for _ in range(nsteps):
            successors = ""
            for predecessor in predecessors:
                if predecessor in self.rules:
                    successors += self.rules[predecessor]
            predecessors = successors
            print(predecessors)
        return predecessors


if __name__ == "__main__":  # pragma: no cover
    test_lsys = Lsys(["A", "B"], {"A": "AB"})
    print(test_lsys.rules)
    test_lsys.add_rules({"B": "AA"})
    print(test_lsys.rules)
    print("hello")
    test_lsys.step("A", 10)
