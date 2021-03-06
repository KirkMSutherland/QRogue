import libtcodpy as libtcod
from game_states import GameStates
from menus import character_screen, inventory_menu, level_up_menu, examine_screen
from enum import Enum

class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, font_color=libtcod.white):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, font_color)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))    
    
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                   screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                back_col = ''
                fore_col = ''

                if visible:
                    if wall:
                        back_col = 'back_light_wall'
                        fore_col = 'fore_light_wall'
                    else:
                        back_col = 'back_light_ground'
                        fore_col = 'fore_light_ground'

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:                        
                    if wall:
                        back_col = 'back_dark_wall'
                        fore_col = 'fore_dark_wall'
                    else:
                        back_col = 'back_dark_ground'
                        fore_col = 'fore_dark_ground'

                if back_col and fore_col:
                    libtcod.console_put_char_ex(con, x, y, game_map.tiles[x][y].char,
                                                colors.get(fore_col),
                                                colors.get(back_col))

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)

    render_bar(panel, 1, 2, bar_width, 'ST', 7, 10,
               libtcod.light_green, libtcod.darker_green)

    render_bar(panel, 1, 3, bar_width, 'MP', 7, 10,
               libtcod.light_blue, libtcod.darker_blue)

    render_bar(panel, 1, 4, bar_width, 'XP', player.level.current_xp, player.level.experience_to_next_level,
               libtcod.light_yellow, libtcod.darker_yellow, font_color=libtcod.white)

    libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon level: {0}'.format(game_map.dungeon_level))

    s = ','
    libtcod.console_print_ex(panel, 1, 6, libtcod.BKGND_NONE, libtcod.LEFT,
                             '{0}'.format(s.join(list(player.fighter.conditions.keys()))))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))    

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.QUICK_USE,
                      GameStates.QUICK_USE_NUMBER):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        elif game_state == GameStates.DROP_INVENTORY:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
        elif game_state == GameStates.QUICK_USE_NUMBER:
            inventory_title = 'Press 1-5 to select a quick use slot'
        elif game_state ==  GameStates.QUICK_USE:
            inventory_title = 'Press the key next to an item to assign it to a quickslot'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 40, 30, screen_width, screen_height)

    elif game_state == GameStates.EXAMINE_SCREEN:
        examine_screen(entities, mouse, fov_map, 40, 30, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):

    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or ((entity.stairs or entity.item or
            entity.render_order == RenderOrder.CORPSE) and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
