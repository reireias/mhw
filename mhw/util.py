#!/usr/bin/env python3
"""
utility module for mhw
"""

from itertools import product
from .damage import Condition, calculate
from . import motionlist


def generate_skill_patterns():
    """
    gererate full pattern contains supported skill
    """
    attack = list(range(0, 8))
    weakness = list(range(0, 4))
    critical_eye = list(range(0, 8))
    maximum_might = list(range(0, 4))
    full_charge = list(range(0, 4))
    critical_boost = list(range(0, 4))
    elemental = list(range(0, 4))
    elemental_critical = list(range(0, 2))
    non_elemental = list(range(0, 2))
    challenger = list(range(0, 6))
    patterns = []
    for skills in product(attack, weakness, critical_eye, maximum_might, full_charge, critical_boost, elemental, elemental_critical, non_elemental, challenger):
        pattern = {}
        pattern['attack'] = skills[0]
        pattern['weakness'] = skills[1]
        pattern['critical_eye'] = skills[2]
        pattern['maximum_might'] = skills[3]
        pattern['full_charge'] = skills[4]
        pattern['critical_boost'] = skills[5]
        pattern['elemental'] = skills[6]
        pattern['elemental_critical'] = skills[7]
        pattern['non_elemental'] = skills[8]
        pattern['challenger'] = skills[9]
        patterns.append(pattern)
    return patterns


def generate_targets():
    """
    target meat condition
    """
    for phy in range(5, 101, 5):
        for ele in range(5, 81, 5):
            yield (phy, ele)


def skill_rank(target, weapon, motion, max_skill_point, exclude_skills=None, include_skills=None):
    """
    ranking by skill patterns
    """
    result = []
    condition = Condition()
    condition.weapon = weapon
    for pattern in generate_skill_patterns():
        # skill point
        skill_point = sum(pattern.values())
        if skill_point > max_skill_point:
            continue

        # exclude
        if exclude_skills is not None:
            skip = False
            for ex_skill in exclude_skills:
                if pattern[ex_skill] > 0:
                    skip = True
                    break
            if skip:
                continue

        # include
        if include_skills is not None:
            skip = False
            for name, level in include_skills.items():
                if pattern[name] != level:
                    skip = True
                    break
            if skip:
                continue

        condition.apply(pattern)
        dmg = calculate(target, motion, condition)
        result.append((dmg, pattern))
    result.sort(key=lambda x: x[0], reverse=True)
    return result
