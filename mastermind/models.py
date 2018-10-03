from django.db import models
from enum import Enum
from enumchoicefield import ChoiceEnum, EnumChoiceField

class Color(ChoiceEnum):
    Red = "R"
    Green = "G"
    Yellow = "Y"
    Blue = "B"
    Magenta = "M"
    Purple = "P"

class ResultColor(ChoiceEnum):
    Black = "Black"
    White = "White"

class Game(models.Model):
    peg1 = EnumChoiceField(Color, default = Color.Green)
    peg2 = EnumChoiceField(Color, default = Color.Green)
    peg3 = EnumChoiceField(Color, default = Color.Green)
    peg4 = EnumChoiceField(Color, default = Color.Green)

    def __str__(self):
        return "GamedId: {}".format(self.id)

class AttemptResponse(models.Model):
    response1 = EnumChoiceField(ResultColor, null = True, blank = True)
    response2 = EnumChoiceField(ResultColor, null = True, blank = True)
    response3 = EnumChoiceField(ResultColor, null = True, blank = True)
    response4 = EnumChoiceField(ResultColor, null = True, blank = True)

    def __str__(self):
        return "Attempt response: {} {} {} {}".format(self.response1, self.response2, self.response3, self.response4)


class Attempt(models.Model):
    peg1 = EnumChoiceField(Color, default = Color.Green)
    peg2 = EnumChoiceField(Color, default = Color.Green)
    peg3 = EnumChoiceField(Color, default = Color.Green)
    peg4 = EnumChoiceField(Color, default = Color.Green)

    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    result = models.OneToOneField(AttemptResponse, on_delete = models.CASCADE, null = True, blank = True)
    
    def __str__(self):
        return "Attempt for game {} values: {} {} {} {}".format(self.game.id, self.peg1, self.peg2, self.peg3, self.peg4)