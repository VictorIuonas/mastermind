from .models import Game, Color
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id',)



