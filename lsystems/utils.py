def rule_str_to_dict(rule_str):
    rule_dict = dict([rule_str.split(" -> ")])
    return rule_dict


def rule_dict_to_str(dict):
    items = dict.items()
    ss = [str(r) + " -> " + str(k) for r, k in items]
    return list(ss)
