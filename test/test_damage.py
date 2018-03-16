#!/usr/bin/env python3
"""
unit test for damage.py
"""

import unittest
from collections import defaultdict
from mhw import Condition, calculate, motionlist, skill_rank, to_label


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
        condition.buff['cylinder'] = 1
        dmg = calculate(target, motion, condition)
        self.assertEqual(524.5, dmg)
        condition.buff['cylinder'] = 0
        condition.skills['weakness'] = 3
        dmg = calculate(target, motion, condition)
        self.assertEqual(524.5, dmg)
        condition.skills['elemental_critical'] = 1
        dmg = calculate(target, motion, condition)
        self.assertEqual(556.5, dmg)

    def test_apply(self):
        """
        test for apply method
        """
        condition = Condition()
        condition.weapon = (230, 0, 0, 'white')
        skills = {'weakness': 3}
        condition.apply(skills)
        # レウス頭
        dmg = calculate((65, 30), [7], condition)
        self.assertEqual(19.5, dmg)

    def test_skill_rank_exclude(self):
        """
        skill_rank method whith exclude argument
        """
        target = (65, 30)
        weapon = (100, 0, 0, 'green')
        motion = motionlist.DUAL_SWORD_A
        rank = skill_rank(target, weapon, motion, 1)
        self.assertEqual(1, rank[0][1]['non_elemental'])
        rank = skill_rank(target, weapon, motion, 1, exclude_skills=['non_elemental'])
        self.assertEqual(1, rank[0][1]['weakness'])

    def test_skill_rank_include(self):
        """
        skill_rank method whith include argument
        """
        target = (65, 30)
        weapon = (100, 0, 0, 'green')
        motion = motionlist.DUAL_SWORD_A
        rank = skill_rank(target, weapon, motion, 2)
        self.assertEqual(1, rank[0][1]['non_elemental'])
        self.assertEqual(1, rank[0][1]['full_charge'])
        rank = skill_rank(target, weapon, motion, 2, include_skills={'weakness': 1})
        self.assertEqual(1, rank[0][1]['non_elemental'])
        self.assertEqual(1, rank[0][1]['weakness'])

    def test_to_label(self):
        """
        to_label test
        """
        pattern = defaultdict(int)
        pattern['attack'] = 2
        pattern['critical_eye'] = 1
        label = to_label(pattern)
        self.assertEqual('攻撃2,見切1', label)
