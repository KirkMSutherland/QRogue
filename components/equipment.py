from components.equipment_slots import EquipmentSlots

class Equipment:
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand is not None:
                if self.main_hand.uID == equippable_entity.uID:
                    self.main_hand = None
                    results.append({'dequipped': equippable_entity})
                else:
                    results.append({'dequipped': self.main_hand})

                    self.main_hand = equippable_entity
                    results.append({'equipped': equippable_entity})
            else:
                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand is not None:
                if self.off_hand.uID == equippable_entity.uID:
                    self.off_hand = None
                    results.append({'dequipped': equippable_entity})
                else:
                    results.append({'dequipped': self.off_hand})

                    self.off_hand = equippable_entity
                    results.append({'equipped': equippable_entity})

            else:
                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results

    def to_json(self):
        json_data = {
            'main_hand': self.main_hand.to_json() if self.main_hand is not None else None,
            'off_hand': self.off_hand.to_json() if self.off_hand is not None else None,
            'defense_bonus': self.defense_bonus,
            'max_hp_bonus': self.max_hp_bonus,
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        from entity import Entity
        main_hand = json_data.get('main_hand')
        off_hand = json_data.get('off_hand')

        equipment = Equipment(Entity.from_json(main_hand) if main_hand else None,
                              Entity.from_json(off_hand) if off_hand else None)

        return equipment