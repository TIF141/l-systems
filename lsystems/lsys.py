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
        # Remove all ignored characters from
        for character in self.ignore:
            predecessors_ignore = predecessors.replace(character, "")
        # print(predecessors_ignore)
        # left_context_rule = [rule.split("<", 1)[0] for rule in self.rules.keys()]
        # right_context_rule = [rule.split(">", 1)[1] for rule in self.rules.keys()]
        # strict_predecessors = [
        #     rule.split("<", 1)[1].split(">", 1)[0] for rule in self.rules.keys()
        # ]

        for i, strict_predecessor in enumerate(predecessors):
            print("Next predecessor")
            if strict_predecessor not in self.ignore:
                # left_context = predecessors[i - 1] if i > 0 else None
                left = [i for i in predecessors[:i] if i not in self.ignore]
                left_context = left[-1] if len(left) > 0 else None
                right = [i for i in predecessors[i + 1 :] if i not in self.ignore]
                # print(left, right)
                right_context = right[0] if len(right) > 0 else None
                # predecessor = predcessors[i]
                # right_context = (
                #     predecessors[i + 1] if i < len(predecessors) - 1 else None
                # )

                # print(left_context, strict_predecessor, right_context)
                # if predecessor is S, left context is left and right context is right
                for key, value in self.rules.items():
                    left_context_rule = key.split("<", 1)[0]
                    right_context_rule = key.split(">", 1)[1]
                    strict_predecessor_rule = key.split("<", 1)[1].split(">", 1)[0]
                    if (
                        strict_predecessor == strict_predecessor_rule
                        and left_context == left_context_rule
                        and right_context == right_context_rule
                    ):
                        print(key, value)
                        successors += value
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
