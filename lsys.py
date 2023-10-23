class Lsys:
    def __init__(self, alphabet, rules):
        self.alphabet = alphabet
        self.rules = rules

    def add_rule(self, newrules):
        for input, output in newrules.items():
            self.rules[input] = output
