from lsystems.generator import Generator
from lsystems.lsys import Lsys

alphabet = ["A", "B"]
rules = {"A": "AB", "B": "AA"}
test_lsys = Lsys(alphabet, rules)
test_gen = Generator(test_lsys, "A", 3)


def test_generate():
    steps = test_gen.generate()
    print(steps)
    assert steps[-1] == "ABAAABAB"
