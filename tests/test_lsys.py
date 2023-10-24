from lsystems.lsys import Lsys

alphabet = ["A", "B"]
rules = {"A": "ABA", "B": "BBB"}
test_lsys = Lsys(alphabet, rules)


def testalphabet():
    assert test_lsys.alphabet == alphabet


def testrules():
    assert test_lsys.rules == rules


def testaddrules():
    test_lsys.add_rules({"AB": "AAA"})
    expectation = {"A": "ABA", "B": "BBB", "AB": "AAA"}
    assert test_lsys.rules == expectation


def teststep():
    predecessor = "A"
    successor = test_lsys.step(predecessor)
    expectation = "ABA"
    assert successor == expectation
