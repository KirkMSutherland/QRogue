from game_messages import Message

class Quickuse:

    def __init__(self, quick_list=[0]*5):
        self.quick_list = quick_list

    def add_item(self, index, item):
        results = []
        self.quick_list[index] = item.uID

        results.append({'item_slotted': True,
                        'message': Message('{0} assigned to slot {1}'.format(item.name, index + 1))})

        return results

    def to_json(self):
        json_data = {
            'quick_list': self.quick_list
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        quick_list_data = json_data.get('quick_list')

        quick_list = Quickuse(quick_list_data)

        return quick_list