import libtcodpy as libtcod

from game_messages import Message

def bleeding(*args, **kwargs):

    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    entity.fighter.take_damage(amount)
    results.append({'message': Message('{0} is bleeding for {1} damage'.format(entity.name, amount), libtcod.red)})

    return results