from django.db import models
from enum import Enum
from enumchoicefield import ChoiceEnum, EnumChoiceField

class Color(ChoiceEnum):
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    Pink = "Pink"
    Purple = "Purple"


class PegCombination(models.Model):
    # I don't know how to create an enum list field
    peg1 = EnumChoiceField(Color)
    peg2 = EnumChoiceField(Color)
    peg3 = EnumChoiceField(Color)
    peg4 = EnumChoiceField(Color)

class Game(models.Model):
    #solution = models.ForeignKey(PegCombination, on_delete = models.CASCADE)

    def __str__(self):
        return "GamedId: {}".format(self.id)

