from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, Color, Attempt
from .serializers import GameSerializer, ColorConverter, AttemptResponseSerilaizer
from .services import value_by_key_prefix, GameFactory, AttemptResponseCalculator, GameHistoryCompiler, AttemptCompiler

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
    attempt_compiler = AttemptCompiler()
    response_calculator = AttemptResponseCalculator()
    response_serializer = AttemptResponseSerilaizer

    def post(self, request, game_id):
        attempt = self.attempt_compiler.build_attempt(request.data, Game.objects.get(id = game_id))
        response = self.response_calculator.calculate(attempt)

        response.save()
        attempt.result = response
        attempt.save()

        serializer = self.response_serializer(response, data = request.data)
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DetailsView(APIView):
    history_compiler = GameHistoryCompiler()

    def get(self, request, pk):
        existing_games = Game.objects.filter(id = pk)

        if len(existing_games) > 0:
            response_data = self.history_compiler.build_history(pk)
            return Response(response_data, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)
