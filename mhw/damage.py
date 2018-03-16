#!/usr/bin/env python3
"""
MHW damage calculator
"""

from collections import defaultdict

# 斬れ味補正(物理)
SHARPNESS = {
    'green': 1.05,
    'white': 1.32
}

# 斬れ味補正(属性)
ELEMENTAL_SHARPNESS = {
    'green': 1.00,
    'white': 1.125
}

# 攻撃 [Level] = (攻撃, 会心)
SKILL_ATTACK = [
    (0, 0),
    (3, 0),
    (6, 0),
    (9, 0),
    (12, 5),
    (15, 5),
    (18, 5),
    (21, 5),
]

# 弱点特効 [Level] = 会心上昇
SKILL_WEAKNESS = [0, 15, 30, 50]

# 見切り [Level] = 会心上昇
SKILL_CRITICAL_EYE = [0, 3, 6, 10, 15, 20, 25, 30]

# 渾身 [Level] = 会心上昇
SKILL_MAXIMUM_MIGHT = [0, 10, 20, 30]

# フルチャージ [Level] = 攻撃上昇
SKILL_FULL_CHARGE = [0, 5, 10, 20]

# 属性強化 [Level] = 属性上昇
SKILL_ELEMENTAL = [0, 3, 6, 10]

# 挑戦者 [Level] = (攻撃, 会心)
SKILL_CHALLENGER = [
    (0, 0),
    (4, 3),
    (8, 6),
    (12, 9),
    (16, 12),
    (20, 15)
]

SUPPORTED_SKILLS = [
    'attack',
    'weakness',
    'critical_eye',
    'maximum_might',
    'full_charge',
    'critical_boost',
    'elemental',
    'elemental_critical',
    'non_elemental',
    'challenger'
]


class Condition:
    """
    conditions(skill, buff, weapon)
    """

    def __init__(self):
        self.skills = defaultdict(int)
        self.buff = defaultdict(int)
        self.weapon = (0, 0, 0, 'white')

    def apply(self, skills):
        """
        apply skill dict to condition
        """
        for skill in SUPPORTED_SKILLS:
            if skill in skills:
                self.skills[skill] = skills[skill]

    def physical_power(self, anger=False):
        """
        display value of physical power
        """
        atk = self.weapon[0]
        # スキル 無属性強化
        if self.skills['non_elemental'] == 1 and self.weapon[1] == 0:
            atk *= 1.1
            atk = round(atk)
        # 護符
        atk += 6
        # 爪
        atk += 9
        # 食事
        atk += 15
        # 鬼人薬
        atk += 7
        # 種
        atk += 10
        # 粉塵
        atk += 10
        # スキル 攻撃
        atk += SKILL_ATTACK[self.skills['attack']][0]
        # スキル フルチャージ
        atk += SKILL_FULL_CHARGE[self.skills['full_charge']]
        # スキル 挑戦者
        if anger:
            atk += SKILL_CHALLENGER[self.skills['challenger']][0]
        return atk

    def elemental_atk(self):
        """
        display value of elemental power
        """
        # 属性強化
        elem = self.weapon[1]
        elem += SKILL_ELEMENTAL[self.skills['elemental']]
        elem = min(elem, self.weapon[1] * 1.3)
        return elem

    # 会心率
    def affinity(self, anger=False):
        """
        display value of affinity
        """
        aff = self.weapon[2]
        # 見切り
        aff += SKILL_CRITICAL_EYE[self.skills['critical_eye']]
        # 攻撃
        aff += SKILL_ATTACK[self.skills['attack']][1]
        # 渾身
        aff += SKILL_MAXIMUM_MIGHT[self.skills['maximum_might']]
        # 達人の円筒
        aff += 50 if self.buff['cylinder'] else 0
        # 挑戦者
        if anger:
            aff += SKILL_CHALLENGER[self.skills['challenger']][1]
        return aff

    # 会心時上昇率
    def critical(self):
        """
        critical damage ratio
        """
        return 1.25 + 0.05 * self.skills['critical_boost']


def calculate(target, motions, condition):
    """
    calculate damage
    """
    anger = False
    if len(target) == 3:
        anger = target[2]
    dmg = 0
    for motion in motions:
        # 物理
        physical = 1
        # モーション値 / 100
        physical *= motion / 100
        # 武器倍率
        physical *= condition.physical_power()
        # 切れ味補正
        physical *= SHARPNESS[condition.weapon[3]]
        # 中腹補正
        physical *= 1.0
        # 怒り補正
        physical *= 1.1 if anger else 1.0
        # 肉質/100
        physical *= target[0] / 100
        # 会心補正
        physicals = [round(physical * 0.75),
                     round(physical),
                     round(physical * condition.critical())]

        affinity = condition.affinity()
        # 弱点特効
        if target[0] >= 45:
            affinity += SKILL_WEAKNESS[condition.skills['weakness']]
        if affinity > 100:
            affinity = 100
        if affinity >= 0:
            physical = (physicals[2] * affinity + physicals[1] * (100 - affinity)) / 100
        else:
            physical = (physicals[1] * (100 + affinity) - physicals[0] * affinity) / 100

        # 属性
        elemental = condition.elemental_atk()
        # 斬れ味補正
        elemental *= ELEMENTAL_SHARPNESS[condition.weapon[3]]
        # 怒り補正
        elemental *= 1.1 if anger else 1.0
        # 肉質
        elemental *= target[1] / 100
        # 属性会心
        if condition.skills['elemental_critical'] and affinity > 0:
            elementals = [round(elemental), round(elemental * 1.35)]
            elemental = (elementals[0] * (100 - affinity) + elementals[1] * affinity) / 100
        elemental = round(elemental)
        dmg = dmg + physical + elemental
    return dmg
