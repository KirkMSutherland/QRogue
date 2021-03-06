import math
import libtcodpy as libtcod
from components import level

from render_functions import RenderOrder

from components.fighter import Fighter
from components.ai import BasicMonster, ConfusedMonster
from components.item import Item
from components.inventory import Inventory
from components.stairs import Stairs
from components.level import Level
from components.item import Item
from components.equipment import Equipment
from components.equippable import Equippable
from components.quick_use import Quickuse

import uuid


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None,uID=None, quick_use=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.quick_use = quick_use

        #TODO check if stackable
        if uID is None:
            self.uID = uuid.uuid4().hex
        else:
            self.uID = uID

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                    get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)
            return True
        else:
            return False

    def move_astar(self, target, entities, game_map, check_explored=False, max_path=25):
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                if check_explored:
                    libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                               not game_map.tiles[x1][y1].blocked and game_map.tiles[x1][y1].explored)
                else:
                    libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                               not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < max_path:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
                return True
            else:
                return False
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            return self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)            

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def to_json(self):
        if self.fighter:
            fighter_data = self.fighter.to_json()
        else:
            fighter_data = None

        if self.ai:
            ai_data = self.ai.to_json()
        else:
            ai_data = None

        if self.item:
            item_data = self.item.to_json()
        else:
            item_data = None

        if self.inventory:
            inventory_data = self.inventory.to_json()
        else:
            inventory_data = None

        if self.stairs:
            stairs_data = self.stairs.to_json()
        else:
            stairs_data = None

        if self.level:
            level_data = self.level.to_json()
        else:
            level_data = None

        if self.equipment:
            equipment_data = self.equipment.to_json()
        else:
            equipment_data = None

        if self.equippable:
            equippable_data = self.equippable.to_json()
        else:
            equippable_data = None

        if self.quick_use:
            quick_use_data = self.quick_use.to_json()
        else:
            quick_use_data = None


        json_data = {
            'x': self.x,
            'y': self.y,
            'char': self.char,
            'color': (self.color[0], self.color[1], self.color[2]),
            'name': self.name,
            'blocks': self.blocks,
            'render_order': self.render_order.value,
            'fighter': fighter_data,
            'ai': ai_data,
            'item': item_data,
            'inventory': inventory_data,
            'stairs': stairs_data,
            'level': level_data,
            'equipment': equipment_data,
            'equippable': equippable_data,
            'uID': self.uID,
            'quick_use': quick_use_data
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        x = json_data.get('x')
        y = json_data.get('y')
        char = json_data.get('char')
        color_o = json_data.get('color')
        color = libtcod.Color(color_o[0], color_o[1], color_o[2])
        name = json_data.get('name')
        blocks = json_data.get('blocks', False)
        render_order = RenderOrder(json_data.get('render_order'))
        fighter_json = json_data.get('fighter')
        ai_json = json_data.get('ai')
        item_json = json_data.get('item')
        inventory_json = json_data.get('inventory')
        stairs_json = json_data.get('stairs')
        level_json = json_data.get('level')
        equipment_json = json_data.get('equipment')
        equippable_json = json_data.get('equippable')
        uID_data = json_data.get('uID')
        quickuse_json = json_data.get('quick_use')

        entity = Entity(x, y, char, color, name, blocks, render_order,uID=uID_data)

        if fighter_json:
            entity.fighter = Fighter.from_json(fighter_json)
            entity.fighter.owner = entity

        if ai_json:
            name = ai_json.get('name')

            if name == BasicMonster.__name__:
                ai = BasicMonster.from_json()
            elif name == ConfusedMonster.__name__:
                ai = ConfusedMonster.from_json(ai_json, entity)
            else:
                ai = None

            if ai:
                entity.ai = ai
                entity.ai.owner = entity

        if item_json:
            entity.item = Item.from_json(item_json)
            entity.item.owner = entity

        if inventory_json:
            entity.inventory = Inventory.from_json(inventory_json)
            entity.inventory.owner = entity

        if stairs_json:
            entity.stairs = Stairs.from_json(stairs_json)
            entity.stairs.owner = entity

        if level_json:
            entity.level = Level.from_json(level_json)
            entity.level.owner = entity

        if equipment_json:
            entity.equipment = Equipment.from_json(equipment_json)
            entity.equipment.owner = entity

        if equippable_json:
            entity.equippable = Equippable.from_json(equippable_json)
            entity.equippable.owner = entity

        if quickuse_json:
            entity.quick_use = Quickuse.from_json(quickuse_json)
            entity.quick_use.owner = entity

        return entity

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
