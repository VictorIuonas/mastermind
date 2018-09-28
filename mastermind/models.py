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

class Combination:
    def __init__(self, pegs):
        self.peg1 = pegs[0]
        self.peg2 = pegs[1]
        self.peg3 = pegs[2]
        self.peg4 = pegs[4]

class PegCombinationField(models.Field):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return Combination([Color.Blue, Color.Blue, Color.Blue, Color.Blue])

    def to_python(self, value):
        if value is None:
            return value
        
        return Combination([Color.Red, Color.Red, Color.Red, Color.Red])


class PegCombination(models.Model):
    # I don't know how to create an enum list field
    peg1 = EnumChoiceField(Color)
    peg2 = EnumChoiceField(Color)
    peg3 = EnumChoiceField(Color)
    peg4 = EnumChoiceField(Color)

class Game(models.Model):
    #solution = PegCombinationField()
    #solution = EnumChoiceField(Color, min_length = 4, max_length = 4)
    peg1 = EnumChoiceField(Color, default = Color.Green)
    peg2 = EnumChoiceField(Color, default = Color.Green)
    peg3 = EnumChoiceField(Color, default = Color.Green)
    peg4 = EnumChoiceField(Color, default = Color.Green)

    def __str__(self):
        return "GamedId: {}".format(self.id)

