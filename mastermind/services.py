from .models import Game, Color, Attempt, AttemptResponse, ResultColor
from .serializers import ColorConverter
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

class GameHistoryCompiler(object):
    def __init__(self):
        self.color_converter = ColorConverter()

    def build_attempt_data(self, attempt):
        result = {}

        result['input'] = {
            'peg1': self.color_converter.from_color(attempt.peg1),
            'peg2': self.color_converter.from_color(attempt.peg2),
            'peg3': self.color_converter.from_color(attempt.peg3),
            'peg4': self.color_converter.from_color(attempt.peg4),
        }

        if attempt.result != None:
            result['result'] = {
                'response1': str(attempt.result.response1),
                'response2': str(attempt.result.response2),
                'response3': str(attempt.result.response3),
                'response4': str(attempt.result.response4),
            }

        return result

    def build_history(self, game_id):
        result = {}

        attempts_array = []

        game_attempts = Attempt.objects.filter(game_id = game_id)

        for attempt in game_attempts:
            attempts_array.append(self.build_attempt_data(attempt))

        result['attempts'] = attempts_array

        return result

class AttemptResponseCalculator(object):
    def generate_peg_list(self, peg_combo):
        result = []

        result.append(peg_combo.peg1)
        result.append(peg_combo.peg2)
        result.append(peg_combo.peg3)
        result.append(peg_combo.peg4)

        return result

    def add_peg_list_to_response(self, peg_list):
        response = AttemptResponse()
        response.response1 = peg_list[0]
        response.response2 = peg_list[1]
        response.response3 = peg_list[2]
        response.response4 = peg_list[3]

        return response

    def calculate(self, attempt):
        solution_pegs = self.generate_peg_list(attempt.game)
        attempt_pegs = self.generate_peg_list(attempt)

        response_pegs = []

        for index, peg in enumerate(attempt_pegs):
            response = None
            if peg == solution_pegs[index]:
                response = ResultColor.Black
            elif peg in solution_pegs:
                response = ResultColor.White
            response_pegs.append(response)

        result = self.add_peg_list_to_response(response_pegs)

        return result
