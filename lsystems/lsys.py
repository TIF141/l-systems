import numpy as np
import re


class Lsys:
    def __init__(self, alphabet, rules, ignore):
        self.alphabet = alphabet
        self.rules = rules
        self.ignore = ignore  # + "[]"

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

    # def step_contextdep(self, predecessors):
    #     successors = ""
    #     for i, strict_predecessor in enumerate(predecessors):
    #         print("Next predecessor")
    #         if strict_predecessor not in self.ignore:
    #             left = [i for i in predecessors[:i] if i not in self.ignore]
    #             left_context = left[-1] if len(left) > 0 else "NaN"

    #             right = [i for i in predecessors[i + 1 :] if i not in self.ignore]
    #             right_context = right[0] if len(right) > 0 else "NaN"

    #             predecessor_context = (
    #                 left_context + "<" + strict_predecessor + ">" + right_context
    #             )
    #             print(predecessor_context)
    #             if predecessor_context in self.rules:
    #                 # print(predecessor_context)
    #                 successors += self.rules[predecessor_context]
    #             else:
    #                 successors += strict_predecessor
    #         else:
    #             successors += strict_predecessor
    #     return successors

    # def step_contextdep(self, predecessors):
    #     successors = ""
    #     for i, strict_predecessor in enumerate(predecessors):
    #         print("Next predecessor")
    #         if strict_predecessor not in self.ignore:
    #             left = [i for i in predecessors[:i] if i not in self.ignore]
    #             if len(left) > 0 and left[-1] == "]":
    #                 left_context = left[len(left) - left[::-1].index("[") - 2]
    #             else:
    #                 left_context = left[-1] if len(left) > 0 else "NaN"

    #             right = [i for i in predecessors[i + 1 :] if i not in self.ignore]
    #             if len(right) > 0 and right[0] == "[":
    #                 right_context = right[right.index("]") + 1]
    #             else:
    #                 right_context = right[0] if len(right) > 0 else "NaN"

    #             predecessor_context = (
    #                 left_context + "<" + strict_predecessor + ">" + right_context
    #             )
    #             if predecessor_context in self.rules:
    #                 print(predecessor_context)
    #                 successors += self.rules[predecessor_context]
    #             else:
    #                 successors += strict_predecessor
    #         else:
    #             successors += strict_predecessor
    #     return successors

    def step_contextdep(self, predecessors):
        # F1F0[F1F1]F0
        successors = ""
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
                    right = [i for i in predecessors[i + 1 :] if i not in self.ignore]
                    right_naive = right[0] if len(right) > 0 else "NaN"
                    right_context = right_naive

                    if left_naive == "]":
                        # print(left)
                        # print(leftinv)
                        count = 0
                        for j, char in enumerate(leftinv):
                            if char == "]":
                                count += 1
                            if char == "[":
                                count -= 1
                            if count == 0 and j > 0:
                                # print(j, char)
                                left_context = leftinv[j + 1]
                                # print(left_context)
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
                        left_context + "<" + strict_predecessor + ">" + right_context
                    )
                    print(left_naive, strict_predecessor, right_naive)
                    print(predecessor_context)
                    if predecessor_context in self.rules:
                        # print(predecessor_context)
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
    print("F1F0[F1F1]F0")
    print(test_lsys.step_contextdep("F1F0[F1[F0F0]F1]F0"))


def get_context(str):
    stack = []
    for i, char in enumerate(str):
        if char == "[":
            stack.append(i)
        # elif char == "]":
        #     stack.pop(-1)
        # print(stack)

        left = str[:i]
        left_naive = left[-1] if len(left) > 0 else "NaN"
        if left_naive == "[":
            left_naive = left[stack[-1] - 1]
        if left_naive == "]":
            left_naive = left[stack[-1] - 1]
            # Only pop after the base of the branch has been returned
            stack.pop(-1)

        print(i, left_naive, stack, left, char)

    strinv = str[::-1]

    for i, char in enumerate(strinv):
        if char == "]":
            stack.append(i)
        # elif char == "]":
        #     stack.pop(-1)
        # print(stack)

        right = strinv[:i]
        right_naive = right[-1] if len(right) > 0 else "NaN"
        if right_naive == "]":
            right_naive = "NaN"
            # right_base = right[: stack[-1]]
            # right_naive = next(
            #     (char for char in right_base[::-1] if char not in ["[", "]"]), None
            # )
        if right_naive == "[":
            right_base = right[: stack[-1]]
            right_naive = next(
                (char for char in right_base[::-1] if char not in ["[", "]"]), None
            )
            # Only pop after the base of the branch has been returned
            stack.pop(-1)

        print(i, right_naive, stack, right, char)
