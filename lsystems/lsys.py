class Lsys:
    def __init__(self, alphabet, rules):
        self.alphabet = alphabet
        self.rules = rules

    def add_rules(self, newrules):
        for predecessor, sucessor in newrules.items():
            self.rules[predecessor] = sucessor


test_lsys = Lsys(["a", "b"], {"A": "ABA"})
print(test_lsys.rules)
test_lsys.add_rules({"B": "BBB"})
print(test_lsys.rules)
print("hello")
