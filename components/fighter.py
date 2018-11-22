import libtcodpy as libtcod

from game_messages import Message

from random import randint


class Fighter:
    def __init__(self, hp, defense, power, xp=0, mp=0, st=0, conditions={}, resists={}, afflictions={}, base_acc=0,
                 base_eva=0):
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
        self.resists = resists
        self.afflictions = afflictions
        self.base_acc = base_acc
        self.base_eva = base_eva

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def take_condition(self, condition):

        results = []
        for x in condition:
            resisted = False

            if x in self.resistance:
                if self.resistance[x] > randint(0, 99):
                    resisted = True

            if resisted:
                results.append({'message': Message('{0} resists the {1} effect!'.format(self.owner.name,
                                                                                        x), libtcod.light_blue)})
            else:
                results.append({'message': Message('{0} is afflicted by {1}'.format(self.owner.name, x),
                                                       libtcod.dark_red)})

                # check if same condition already applied, if so then apply greatest magnitude and add duration
                if x in self.conditions:
                    new_duration, new_magnitude = condition[x]
                    duration, magnitude = self.conditions[x]
                    magnitude = max(new_magnitude, magnitude)
                    duration += new_duration

                    self.conditions[x] = [duration, magnitude]
                else:
                    self.conditions[x] = condition[x]

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
            if self.afflict:
                target.fighter.take_condition(self.afflict)
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results

    @property
    def resistance(self):
        bonus = {}
        bonus.update(self.resists)
        if self.owner and self.owner.equipment:
            bonus.update(self.owner.equipment.resistance_bonus)

        return bonus

    @property
    def afflict(self):
        bonus = {}
        bonus.update(self.afflictions)
        if self.owner and self.owner.equipment:
            bonus.update(self.owner.equipment.affliction_bonus)

        return bonus


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
            'conditions': self.conditions,
            'resists': self.resists,
            'afflictions': self.afflictions,
            'base_acc': self.base_acc,
            'base_eva': self.base_eva
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
        resists = json_data.get('resists')
        afflictions = json_data.get('afflictions')
        base_eva = json_data.get('base_eva')
        base_acc = json_data.get('base_acc')

        fighter = Fighter(base_max_hp, defense, power, xp)
        fighter.hp = hp
        fighter.st = st
        fighter.mp = mp
        fighter.max_st = max_st
        fighter.base_max_mp = base_max_mp
        fighter.conditions = conditions
        fighter.resists = resists
        fighter.afflictions = afflictions
        fighter.base_eva = base_eva
        fighter.base_acc = base_acc

        return fighter
