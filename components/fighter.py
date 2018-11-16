import libtcodpy as libtcod

from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, power, xp=0, mp=0, st=0, conditions={}):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.base_max_mp = mp
        self.mp = mp
        self.base_max_st = st
        self.st = st
        self.conditions = conditions

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        damage = self.power - target.fighter.defense
        results = []

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def to_json(self):
        json_data = {
            'base_max_hp': self.base_max_hp,
            'hp': self.hp,
            'base_defense': self.base_defense,
            'base_power': self.base_power,
            'xp': self.xp,
            'base_max_mp': self.base_max_mp,
            'mp': self.mp,
            'base_max_st': self.base_max_st,
            'st': self.st,
            'conditions': self.conditions
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        base_max_hp = json_data.get('base_max_hp')
        hp = json_data.get('hp')
        defense = json_data.get('base_defense')
        power = json_data.get('base_power')
        xp = json_data.get('xp')
        max_st = json_data.get('max_st')
        st = json_data.get('st')
        base_max_mp = json_data.get('base_max_mp')
        mp = json_data.get('mp')
        conditions = json_data.get('conditions')

        fighter = Fighter(base_max_hp, defense, power, xp)
        fighter.hp = hp
        fighter.st = st
        fighter.mp = mp
        fighter.max_st = max_st
        fighter.base_max_mp = base_max_mp
        fighter.conditions = conditions

        return fighter
