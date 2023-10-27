import numpy as np


class Lsys:
    def __init__(self, alphabet, rules, ignore="+-F"):
        self.alphabet = alphabet
        self.rules = rules
        self.ignore = ignore  # + "[]"

    def add_rules(self, newrules):
        for predecessor, successor in newrules.items():
            self.rules[predecessor] = successor

    def step(self, predecessors):
        successors = ""

        # If rules are context dependent
        if any(("<" or ">") in key for key in self.rules.keys()):
            for i, strict_predecessor in enumerate(predecessors):
                if strict_predecessor not in ("F[]"):  # NEED TO CHANGE THIS
                    print(f"Next predecessor {i}")

                    if "*<" + strict_predecessor + ">*" in self.rules:
                        successors += self.rules["*<" + strict_predecessor + ">*"]
                    else:
                        left = [i for i in predecessors[:i] if i not in self.ignore]
                        leftinv = left[::-1]
                        left_naive = left[-1] if len(left) > 0 else "NaN"
                        left_context = left_naive
                        right = [
                            i for i in predecessors[i + 1 :] if i not in self.ignore
                        ]
                        right_naive = right[0] if len(right) > 0 else "NaN"
                        right_context = right_naive

                        # Find left_context
                        if left_naive == "]":
                            count = 0
                            for j, char in enumerate(leftinv):
                                if char == "]":
                                    count += 1
                                if char == "[":
                                    count -= 1
                                if count == 0 and j > 0:
                                    left_context = leftinv[j + 1]
                                    break

                        if left_naive == "[":
                            count = 0
                            # skip out the first element of leftinv - i.e. the bracket
                            for j, char in enumerate(leftinv[1:]):
                                if char == "]":
                                    count += 1
                                if char == "[":
                                    count -= 1
                                if count == 0 and char not in ["[", "]"]:
                                    left_context = leftinv[j + 1]
                                    break

                        # Find right context
                        if right_naive == "[":
                            count = 0
                            for j, char in enumerate(right):
                                if char == "[":
                                    count += 1
                                if char == "]":
                                    count -= 1
                                if count == 0 and j > 0:
                                    right_context = right[j + 1]
                                    break

                        if right_naive == "]":
                            right_context = "NaN"

                        predecessor_context = (
                            left_context
                            + "<"
                            + strict_predecessor
                            + ">"
                            + right_context
                        )
                        print(left_naive, strict_predecessor, right_naive)
                        print(predecessor_context)
                        if predecessor_context in self.rules:
                            # print(predecessor_context)
                            successors += self.rules[predecessor_context]
                            # print(successors)
                        else:
                            successors += strict_predecessor
                else:
                    successors += strict_predecessor

        # If rules are not context dependent, step normally
        else:
            for predecessor in predecessors:
                if predecessor in self.rules:
                    successors += self.rules[predecessor]
                else:
                    successors += predecessor
        # print(predecessors)
        # print(successors)
        return successors


if __name__ == "__main__":  # pragma: no cover
    # test_lsys_1 = Lsys(["A", "B"], {"A": "AB"})
    # print(test_lsys.rules)
    # test_lsys.add_rules({"B": "AA"})
    # print(test_lsys.rules)
    # print("hello")
    # print(test_lsys_1.step("AB"))

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
    # print(test_lsys.step("F1F0[F1F1]F0"))
    print(test_lsys.step("F1F0[F1[F0F0]F1]F0"))
