import libtcodpy as libtcod

from game_messages import Message

class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp

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

    def to_json(self):
        json_data = {
            'max_hp': self.max_hp,
            'hp': self.hp,
            'defense': self.defense,
            'power': self.power,
            'xp': self.xp
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        max_hp = json_data.get('max_hp')
        hp = json_data.get('hp')
        defense = json_data.get('defense')
        power = json_data.get('power')
        xp = json_data.get('xp')

        fighter = Fighter(max_hp, defense, power, xp)
        fighter.hp = hp

        return fighter