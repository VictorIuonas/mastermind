from .models import Game, Color, Attempt, AttemptResponse
from rest_framework import serializers
from enumchoicefield import EnumChoiceField

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        #fields = '__all__'
        fields = ('id',)

class AttemptResponseSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = AttemptResponse
        fields = '__all__'

class AttemptSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only = True)
    result = AttemptResponseSerilaizer()

    class Meta:
        model = Attempt
        fields = '__all__'

    id = serializers.UUIDField(read_only = True)
    peg1 = EnumChoiceField(enum_class = Color)
    peg2 = EnumChoiceField(enum_class = Color)
    peg3 = EnumChoiceField(enum_class = Color)
    peg4 = EnumChoiceField(enum_class = Color)

class ColorConverter():

    def __init__(self):
        self.color_translator = { 
            str(Color.Red): Color.Red, 
            str(Color.Green): Color.Green, 
            str(Color.Yellow): Color.Yellow, 
            str(Color.Blue): Color.Blue, 
            str(Color.Magenta): Color.Magenta, 
            str(Color.Purple): Color.Purple 
        }
        self.inverted_translator = {v: k for k, v in self.color_translator.items()}
    
    def to_color(self, input):
        if input in self.color_translator:
            return self.color_translator[input]
        
        raise Exception('Unknown color: {}'.format(input))

    def from_color(self, input):
        if input in self.inverted_translator:
            return self.inverted_translator[input]

        raise Exception('Unknown color code: {}'.format(input))

    
