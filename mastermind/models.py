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

class Game(models.Model):
    peg1 = EnumChoiceField(Color, default = Color.Green)
    peg2 = EnumChoiceField(Color, default = Color.Green)
    peg3 = EnumChoiceField(Color, default = Color.Green)
    peg4 = EnumChoiceField(Color, default = Color.Green)

    def __str__(self):
        return "GamedId: {}".format(self.id)

