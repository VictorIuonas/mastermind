from .models import Game, Color
from random import randint, seed

def value_by_key_prefix(input_dict, prefix):
    matches = [val for key, val in input_dict.iteritems() if key.startswith(prefix)]
    if not matches:
        raise KeyError(prefix)
    if len(matches) > 1:
        raise ValueError('{} matches more than one key'.format(prefix))

    return matches[0]

class GameFactory(object):
    
    def __init__(self):
        seed()
        self.color_list = list(Color)

    def create(self):
        color_count = len(self.color_list)
        result = Game()

        selected_colors = []
        for i in range(4):
            color_index = randint(0, color_count - 1)
            selected_colors.append(self.color_list[color_index])

        result.peg1 = selected_colors[0]
        result.peg2 = selected_colors[1]
        result.peg3 = selected_colors[2]
        result.peg4 = selected_colors[3]
         
        return result