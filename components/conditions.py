from components.status_type import StatusType

class Conditions:
    def __init__(self):
        self.effects = []

    def add_effect(self, status):
        self.effects.append(status)



    def to_json(self):
        json_data = {
            'effects': [status.to_json() for status in self.effects]
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        from components.status import Status

        effects_json = json_data.get('effects')

        effects = [Status.from_json(effect_json) for effect_json in effects_json]

        conditions = Conditions()
        conditions.effects = effects

        return conditions