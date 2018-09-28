from .models import Game, PegCombination, Color
from rest_framework import serializers

class PegCombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PegCombination
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    solution = PegCombinationSerializer(required = False)

    class Meta:
        model = Game
        fields = '__all__'

    #def create(self, validated_data):
        #solution = PegCombination(peg1 = Color.Blue, peg2 = Color.Blue, peg3 = Color.Blue, peg4 = Color.Blue)
        #solution.save()

        #game = super.create(validated_data)
        #game.solution = solution
        #game.save()

        #return game



