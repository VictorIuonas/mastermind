from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, Color, Attempt
from .serializers import GameSerializer, AttemptSerializer, ColorConverter
from .services import value_by_key_prefix, GameFactory

class CreateGameView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    factory = GameFactory()

    def create(self, request, *args, **kwargs):
        game = self.factory.create()
        game.save()

        serializer = self.serializer_class(game, data = request.data)
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serialier.errors, status = status.HTTP_400_BAD_REQUEST)
        
class AttemptView(APIView):
    color_translator = ColorConverter()

    def post(self, request, game_id):
        attempt = Attempt()
        attempt.game = Game.objects.get(pk = game_id)
        attempt.peg1 = self.color_translator.to_color(request.data['peg1'][0])
        attempt.peg2 = self.color_translator.to_color(request.data['peg2'][0])
        attempt.peg3 = self.color_translator.to_color(request.data['peg3'][0])
        attempt.peg4 = self.color_translator.to_color(request.data['peg4'][0])
        attempt.save()

        return Response(status = status.HTTP_201_CREATED)

class DetailsView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
