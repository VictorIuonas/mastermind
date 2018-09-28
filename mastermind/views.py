from rest_framework import viewsets
from rest_framework import generics

from .models import Game
from .serializers import GameSerializer

class CreateView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

#class GameViewSet(viewsets.ModelViewSet):
#    queryset = Game.objects.all()
#    serializer_class = GameSerializer

#    def create(self, request):
#        serializer = GameSerializer(data = request.data)
#        if serializer.is_valid():
#            game = serializer.save()
#            return Response()

