#!/usr/bin/env python3
"""
"""

import unittest
from mhw import Condition, calculate, motionlist

class TestCalculate(unittest.TestCase):
    """
    """

    def test_calculate(self):
        condition = Condition()
        condition.weapon = (230, 0, 0, 'white')
        # レウス頭
        dmg = calculate((65, 30), [7], condition)
        self.assertEqual(17.0, dmg)

    def test_skills_weakness(self):
        condition = Condition()
        condition.weapon = (230, 0, 0, 'white')
        condition.skills['weakness'] = 3
        # レウス頭
        dmg = calculate((65, 30), [7], condition)
        self.assertEqual(19.5, dmg)

    def test_skills_critical_eye(self):
        condition = Condition()
        condition.weapon = (230, 0, 0, 'white')
        condition.skills['critical_eye'] = 7
        # レウス頭
        dmg = calculate((65, 30), [7], condition)
        self.assertEqual(18.5, dmg)
        condition.skills['attack'] = 7
        # レウス頭
        dmg = calculate((65, 30), [7], condition)
        self.assertEqual(19.75, dmg)

    def test_elemental(self):
        condition = Condition()
        # 超絶
        condition.weapon = (140, 27, 0, 'white')
        # レウス頭
        target = (65, 30)
        # 乱舞
        motion = [17, 17, 6, 6, 10, 10, 9, 9, 11, 11, 9, 9, 12, 12, 7, 20]
        dmg = calculate(target, motion, condition)
        print(dmg)
        condition.skills['elemental'] = 3
        dmg = calculate(target, motion, condition)
        print(dmg)
        condition.skills['weakness'] = 3
        dmg = calculate(target, motion, condition)
        print(dmg)
        condition.skills['elemental_critical'] = 1
        dmg = calculate(target, motion, condition)
        print(dmg)
