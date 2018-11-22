from components.equipment_slots import EquipmentSlots

class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0, resist={}, affliction={}):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.resist = resist
        self.affliction = affliction

    def to_json(self):
        json_data = {
            'slot': self.slot.value,
            'power_bonus': self.power_bonus,
            'defense_bonus': self.defense_bonus,
            'max_hp_bonus': self.max_hp_bonus,
            'resist': self.resist,
            'affliction': self.affliction
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        slot = json_data.get('slot')
        power_bonus = json_data.get('power_bonus')
        defense_bonus = json_data.get('defense_bonus')
        max_hp_bonus = json_data.get('max_hp_bonus')
        resist = json_data.get('resist')
        affliction = json_data.get('affliction')

        equippable = Equippable(EquipmentSlots(slot), power_bonus, defense_bonus, max_hp_bonus, resist, affliction)

        return equippable