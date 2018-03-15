#!/usr/bin/env python3
"""
unit test for damage.py
"""

import unittest
from mhw import Condition, calculate, motionlist


class TestCalculate(unittest.TestCase):
    """
    unit test for damage.py
    """

    def test_calculate(self):
        """
        standard
        """
        condition = Condition()
        condition.weapon = (230, 0, 0, 'white')
        # レウス頭
        dmg = calculate((65, 30), [7], condition)
        self.assertEqual(17.0, dmg)

    def test_skills_weakness(self):
        """
        skill weakness
        """
        condition = Condition()
        condition.weapon = (230, 0, 0, 'white')
        condition.skills['weakness'] = 3
        # レウス頭
        dmg = calculate((65, 30), [7], condition)
        self.assertEqual(19.5, dmg)

    def test_skills_critical_eye(self):
        """
        skill critical eye
        """
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
        """
        skills elemental
        """
        condition = Condition()
        # 超絶
        condition.weapon = (140, 27, 0, 'white')
        # レウス頭
        target = (65, 30)
        # 乱舞
        motion = motionlist.DUAL_SWORD_A
        dmg = calculate(target, motion, condition)
        self.assertEqual(440.0, dmg)
        condition.skills['elemental'] = 3
        dmg = calculate(target, motion, condition)
        self.assertEqual(488.0, dmg)
        condition.skills['weakness'] = 3
        dmg = calculate(target, motion, condition)
        self.assertEqual(524.5, dmg)
        condition.skills['elemental_critical'] = 1
        dmg = calculate(target, motion, condition)
        self.assertEqual(556.5, dmg)
