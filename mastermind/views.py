from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.response import Response

from .models import Game, Color
from .serializers import GameSerializer

class CreateView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        print('is create called')
        game = Game()
        default_color = Color.Red
        game.peg1 = default_color
        game.peg2 = default_color
        game.peg3 = default_color
        game.peg4 = default_color
        serializer = self.serializer_class(game, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serialier.errors, status = status.HTTP_400_BAD_REQUEST)
        

class DetailsView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
