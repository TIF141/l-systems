class Lsys:
    def __init__(self, alphabet, rules):
        self.alphabet = alphabet
        self.rules = rules

    def add_rule(self, newrules):
        for predecessor, sucessor in newrules.items():
            self.rules[predecessor] = sucessor

test_lsys = Lsys(["a","b"],{"A":"ABA"})
print(test_lsys.rules)
test_lsys.add_rule({"B":"BBB"})
print(test_lsys.rules)