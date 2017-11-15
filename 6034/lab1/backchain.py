from production import AND, OR, match, populate, simplify
from collections import ChainMap

def rule_consequent_matches_hypothesis(rule, hypothesis):
    return map(lambda c: c == hypothesis or match(c, hypothesis), rule.consequent())

only_dicts = lambda x: isinstance(x, dict)

def merge(obj):
    return dict(ChainMap(*filter(only_dicts, obj)))

def backchain_to_goal_tree(rules, hypothesis):
    matching_rules = [r for r in rules
        if any(rule_consequent_matches_hypothesis(r, hypothesis))
    ]
    if len(matching_rules) == 0:
        return hypothesis

    subtrees = []
    for rule in matching_rules:
        binding = merge(
            rule_consequent_matches_hypothesis(rule, hypothesis)
        )
        subtree = antecedent_goal_tree(rule, rules, binding)
        subtrees.append(subtree)

    return simplify(OR(hypothesis, *subtrees))

def antecedent_goal_tree(rule, rules, binding):
    antedecents = rule.antecedent()

    if isinstance(antedecents, str):
        return backchain_to_goal_tree(rules, populate(antedecents, binding))

    subtrees = []
    for antedecent in antedecents:
        subtree = backchain_to_goal_tree(rules, populate(antedecent, binding))
        subtrees.append(subtree)

    return type(antedecents)(*subtrees)
