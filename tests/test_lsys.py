from lsys import Lsys

def testalphabet():
    alphabet = ["a", "b"]
    rules = { "A" : "ABA" , "B" : "BBB"}
    test_lsys = Lsys(alphabet, rules)

    assert test_lsys.alphabet == alphabet

def testrules():
    alphabet = ["a", "b"]
    rules = { "A" : "ABA" , "B" : "BBB"}
    test_lsys = Lsys(alphabet, rules)

    assert test_lsys.rules == rules