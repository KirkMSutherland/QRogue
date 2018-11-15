from random import randint


class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, blocked, block_sight=None, char=' '):
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False

        self.char = char

    def to_json(self):
        json_data = {
            'blocked': self.blocked,
            'block_sight': self.block_sight,
            'explored': self.explored,
            'char': self.char
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        blocked = json_data.get('blocked')
        block_sight = json_data.get('block_sight')
        explored = json_data.get('explored')
        char_data = json_data.get('char')

        tile = Tile(blocked, block_sight, char=char_data)
        tile.explored = explored

        return tile
