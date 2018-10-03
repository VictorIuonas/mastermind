from django.db import models
from enum import Enum
from enumchoicefield import ChoiceEnum, EnumChoiceField

class Color(ChoiceEnum):
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    Magenta = "Magenta"
    Purple = "Purple"

class ResultColor(ChoiceEnum):
    Black = "Black"
    White = "White"

class Game(models.Model):
    # Future improvements: peg1 - peg4 should be an array
    peg1 = EnumChoiceField(Color, default = Color.Green)
    peg2 = EnumChoiceField(Color, default = Color.Green)
    peg3 = EnumChoiceField(Color, default = Color.Green)
    peg4 = EnumChoiceField(Color, default = Color.Green)
    # Future improvement - I would add a boolean field in the response stating if the game was won or not
    def __str__(self):
        return "GamedId: {}".format(self.id)

class AttemptResponse(models.Model):
    # Future improvements: response1 - response4 should be an array
    response1 = EnumChoiceField(ResultColor, null = True, blank = True)
    response2 = EnumChoiceField(ResultColor, null = True, blank = True)
    response3 = EnumChoiceField(ResultColor, null = True, blank = True)
    response4 = EnumChoiceField(ResultColor, null = True, blank = True)

    def __str__(self):
        return "Attempt response: {} {} {} {}".format(self.response1, self.response2, self.response3, self.response4)


class Attempt(models.Model):
    # Future improvements: peg1 - peg4 should be an array
    peg1 = EnumChoiceField(Color, default = Color.Green)
    peg2 = EnumChoiceField(Color, default = Color.Green)
    peg3 = EnumChoiceField(Color, default = Color.Green)
    peg4 = EnumChoiceField(Color, default = Color.Green)

    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    result = models.OneToOneField(AttemptResponse, on_delete = models.CASCADE, null = True, blank = True)
    
    def __str__(self):
        return "Attempt for game {} values: {} {} {} {}".format(self.game.id, self.peg1, self.peg2, self.peg3, self.peg4)