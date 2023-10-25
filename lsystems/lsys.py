import numpy as np


class Lsys:
    def __init__(self, alphabet, rules, ignore):
        self.alphabet = alphabet
        self.rules = rules
        self.ignore = ignore

    def add_rules(self, newrules):
        for predecessor, successor in newrules.items():
            self.rules[predecessor] = successor

    def step(self, predecessors):
        successors = ""
        for predecessor in predecessors:
            if predecessor in self.rules:
                successors += self.rules[predecessor]
            else:
                successors += predecessor
        return successors

    def step_contextdep(self, predecessors):
        successors = ""
        for i, strict_predecessor in enumerate(predecessors):
            print("Next predecessor")
            if strict_predecessor not in self.ignore:
                left = [i for i in predecessors[:i] if i not in self.ignore]
                left_context = left[-1] if len(left) > 0 else "NaN"
                right = [i for i in predecessors[i + 1 :] if i not in self.ignore]
                right_context = right[0] if len(right) > 0 else "NaN"
                predecessor_context = (
                    left_context + "<" + strict_predecessor + ">" + right_context
                )
                if predecessor_context in self.rules:
                    print(predecessor_context)
                    successors += self.rules[predecessor_context]
                else:
                    successors += strict_predecessor
            else:
                successors += strict_predecessor
        return successors


if __name__ == "__main__":  # pragma: no cover
    # test_lsys = Lsys(["A", "B"], {"A": "AB"})
    # print(test_lsys.rules)
    # test_lsys.add_rules({"B": "AA"})
    # print(test_lsys.rules)
    # print("hello")
    # test_lsys.step("A", 10)
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
    print("F1F1F1")
    print(test_lsys.step_contextdep("F0F0F1"))
