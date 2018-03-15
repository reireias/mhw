#!/usr/bin/env python3
"""
Damage calculator
"""

from collections import defaultdict


class Condition:
    """
    """

    def __init__(self):
        self.skills = defaultdict(int)
        self.weapon = (100, 10, 0)

    def physical_atk(self):
        return self.weapon[0]

    def elemental_atk(self):
        return self.weapon[1]


def calculate(target, motions, condition):
    dmg = 0
    for motion in motions:
        physical = int(target[0] * condition.physical_atk() * motion / 100 / 100)
        elemental = int(target[1] * condition.elemental_atk() / 100)
        dmg = dmg + physical + elemental
    return dmg
